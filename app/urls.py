from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home-hero-image.jpg", views.home_hero_image, name="home_hero_image"),
    path("page-hero-image/<slug:course_slug>.jpg", views.page_hero_image, name="page_hero_image"),
    path("media-assets/<slug:asset_name>/", views.public_media_asset, name="public_media_asset"),
    path("matematicheskoe-modelirovanie/", views.course_matmodel, name="course_matmodel"),
    path("teoriya-veroyatnostei/", views.course_probability, name="course_probability"),
    path("chislennye-metody/", views.course_numerical, name="course_numerical"),
    path("diskretnaya-matematika/", views.course_discrete, name="course_discrete"),
    path(
        "materials/view/<slug:course_slug>/<slug:material_slug>/",
        views.material_viewer,
        name="material_viewer",
    ),
    path(
        "materials/file/<slug:course_slug>/<slug:material_slug>/",
        views.material_file,
        name="material_file",
    ),
]
