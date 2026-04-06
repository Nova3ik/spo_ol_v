from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from pypdf import PdfReader

from .course_data import COURSES

COURSE_HERO_IMAGES = {
    "mathematical-modeling": "mathbackground.jpg",
    "probability-theory": "terver.jpg",
    "numerical-methods": "seamless-illustration.jpg",
    "discrete-math": "I1KoN.jpg",
}

COURSE_HERO_SUBTITLES = {
    "mathematical-modeling": "Модели, анализ результатов и практические занятия по прикладным математическим задачам.",
    "probability-theory": "Случайные события, распределения и статистические методы для анализа данных.",
    "numerical-methods": "Приближённые вычисления, интерполяция и численные подходы к решению математических задач.",
    "discrete-math": "Логика, множества, отношения и графы с разбором прикладных примеров.",
}


def _serve_media_asset(filename, content_type, not_found_message):
    file_path = settings.MEDIA_ROOT / filename

    if not file_path.is_file():
        raise Http404(not_found_message)

    response = FileResponse(file_path.open("rb"), content_type=content_type)
    response["Cache-Control"] = "public, max-age=86400"
    response["X-Content-Type-Options"] = "nosniff"
    return response


def home(request):
    return render(request, "home.html")


def home_hero_image(request):
    return _serve_media_asset("mathbackground.jpg", "image/jpeg", "Home hero image not found.")


def page_hero_image(request, course_slug):
    filename = COURSE_HERO_IMAGES.get(course_slug)
    if not filename:
        raise Http404("Page hero image not found.")

    return _serve_media_asset(filename, "image/jpeg", "Page hero image not found.")


def favicon(request):
    return _serve_media_asset("favicon.png", "image/png", "Favicon not found.")


def _get_course_hero_context(course_slug):
    return {
        "hero_image_url": reverse("page_hero_image", kwargs={"course_slug": course_slug}),
        "hero_eyebrow": "Дисциплина",
        "hero_subtitle": COURSE_HERO_SUBTITLES[course_slug],
    }


def _get_course(course_slug):
    course = COURSES.get(course_slug)
    if not course:
        raise Http404("Курс не найден.")
    return {"slug": course_slug, **course}


def _get_material(course_slug, material_slug):
    course = _get_course(course_slug)
    for topic in course["topics"]:
        for material in topic["materials"]:
            if material["slug"] == material_slug:
                return course, topic, material
    raise Http404("Материал не найден.")


def _get_material_path(material):
    if not material["is_available"] or not material["file"]:
        raise Http404("Материал недоступен.")

    media_root = (settings.BASE_DIR / "media").resolve()
    allowed_root = (media_root / "lection_material").resolve()
    file_path = (media_root / Path(material["file"])).resolve()

    if file_path.suffix.lower() != ".pdf":
        raise Http404("Поддерживаются только PDF-файлы.")

    try:
        file_path.relative_to(allowed_root)
    except ValueError as exc:
        raise Http404("Недопустимый путь к файлу.") from exc

    if not file_path.is_file():
        raise Http404("PDF-файл не найден.")

    return file_path


def course_matmodel(request):
    return render(request, "course_matmodel.html", _get_course_hero_context("mathematical-modeling"))


def course_probability(request):
    return render(request, "course_probability.html", _get_course_hero_context("probability-theory"))


def course_numerical(request):
    return render(request, "course_numerical.html", _get_course_hero_context("numerical-methods"))


def course_discrete(request):
    return render(request, "course_discrete.html", _get_course_hero_context("discrete-math"))


def material_viewer(request, course_slug, material_slug):
    course, topic, material = _get_material(course_slug, material_slug)
    file_path = _get_material_path(material)
    hero_context = _get_course_hero_context(course_slug)
    reader = PdfReader(str(file_path))
    page_count = len(reader.pages)
    total_page_ratio = 0

    for page in reader.pages:
        width = float(page.mediabox.width or 1)
        height = float(page.mediabox.height or 1)
        total_page_ratio += height / width

    return render(
        request,
        "materials/pdf_viewer.html",
        {
            "course": course,
            "topic": topic,
            "material": material,
            "hero_image_url": hero_context["hero_image_url"],
            "hero_eyebrow": course["title"],
            "hero_subtitle": topic["title"],
            "page_count": max(page_count, 1),
            "total_page_ratio": total_page_ratio or 1,
        },
    )


@xframe_options_sameorigin
def material_file(request, course_slug, material_slug):
    _, _, material = _get_material(course_slug, material_slug)
    file_path = _get_material_path(material)

    response = FileResponse(file_path.open("rb"), content_type="application/pdf")
    response["Content-Disposition"] = "inline"
    response["X-Content-Type-Options"] = "nosniff"
    response["Cross-Origin-Resource-Policy"] = "same-origin"
    return response
