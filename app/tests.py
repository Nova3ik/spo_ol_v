from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from django.views import defaults


class CoursePagesTests(TestCase):
    def test_course_pages_render_test_cta_tooltip(self):
        course_pages = (
            "course_matmodel",
            "course_probability",
            "course_numerical",
            "course_discrete",
        )

        for url_name in course_pages:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'class="test-cta"', count=1)
                self.assertContains(response, 'class="test-cta__info"', count=1)
                self.assertContains(response, '/media/Notebook.svg', count=1)
                self.assertContains(response, 'role="tooltip"', count=1)
                self.assertContains(
                    response,
                    "Данные результата теста отправляются к преподавателю",
                    count=1,
                )

    def test_matmodel_course_page_contains_updated_test_links(self):
        response = self.client.get(reverse("course_matmodel"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "https://docs.google.com/forms/d/e/1FAIpQLScNFffyPsiqE8v73M3UJAGT_edtwcDz5RWqjtHj20k_ls2_yw/viewform?usp=dialog",
            count=1,
        )
        self.assertContains(
            response,
            "https://docs.google.com/forms/d/e/1FAIpQLSfsUKlTUsdObmFF7kZfmz1iOUlxXEmRqdD2tG-nFnOSerQKzA/viewform?usp=dialog",
            count=1,
        )
        self.assertContains(
            response,
            "https://docs.google.com/forms/d/e/1FAIpQLSdS3s4kutZ4w1P6dOcXAedx-7Hd2wiNQvI0Yd_l-ut-dDcxKA/viewform?usp=dialog",
            count=1,
        )

    def test_discrete_course_page_contains_updated_main_test_link(self):
        response = self.client.get(reverse("course_discrete"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "https://docs.google.com/forms/d/e/1FAIpQLSecqPoa9KbAX1jwg6-nihV2_g1RhC0CrK6ITvndHwoO18HBIg/viewform?usp=dialog",
            count=1,
        )

    def test_discrete_course_page_renders_material_links(self):
        response = self.client.get(reverse("course_discrete"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse("material_viewer", args=["discrete-math", "boolean-functions"]),
        )
        self.assertContains(response, "/media/diestel-obl%20.png", count=1)
        self.assertContains(
            response,
            "https://docs.google.com/forms/d/e/1FAIpQLSfqMcbR8fQiVMitvAHAmMSV2Dzb06w1Icx9Vz59BNdYxhuhKA/viewform?usp=dialog",
            count=1,
        )

    def test_material_viewer_renders_internal_file_route(self):
        response = self.client.get(
            reverse("material_viewer", args=["discrete-math", "boolean-functions"])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse("material_file", args=["discrete-math", "boolean-functions"]),
        )
        self.assertContains(response, 'class="pdf-back-link"')
        self.assertContains(response, 'data-total-ratio="')

    def test_probability_course_page_contains_bernoulli_material(self):
        response = self.client.get(reverse("course_probability"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "https://docs.google.com/forms/d/e/1FAIpQLSfZzcQezed6M1sAPFf-UZG1AAPXH2AWlOIPpKtpWphSFTPkwg/viewform?usp=dialog",
            count=1,
        )
        self.assertContains(
            response,
            reverse("material_viewer", args=["probability-theory", "bernoulli-formula"]),
        )
        self.assertContains(
            response,
            "https://docs.google.com/forms/d/e/1FAIpQLScLF7D2mX3RsxH02cu1d8KCRZ42aSIL8UZnIUOjw4MqTTzu1A/viewform?usp=dialog",
            count=1,
        )
        self.assertContains(
            response,
            "https://docs.google.com/forms/d/e/1FAIpQLSeSZWVIbyYUwWrafOGThKHTwZAljAM458Lo8qFEb9T9oce2CQ/viewform?usp=dialog",
            count=1,
        )

    def test_numerical_course_page_contains_updated_main_test_link(self):
        response = self.client.get(reverse("course_numerical"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "https://docs.google.com/forms/d/e/1FAIpQLSffUi-BWgwtwzN4o86Iq-JgRYcmBOgm7v6LOLFo_ZWuxNHCow/viewform?usp=dialog",
            count=1,
        )

    def test_material_file_returns_pdf_response(self):
        response = self.client.get(
            reverse("material_file", args=["discrete-math", "boolean-functions"])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertEqual(response["Content-Disposition"], "inline")

    def test_unavailable_material_viewer_returns_404(self):
        response = self.client.get(
            reverse(
                "material_viewer",
                args=["probability-theory", "distributions-placeholder-1"],
            )
        )

        self.assertEqual(response.status_code, 404)


class ErrorPagesTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
    def test_404_page_renders_custom_template(self):
        response = self.client.get("/stranitsa-kotoroi-net/")

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Страница не найдена", status_code=404)
        self.assertContains(response, reverse("home"), status_code=404)
        self.assertContains(response, 'class="error-panel__backdrop"', status_code=404)
        self.assertNotContains(response, 'class="site-header"', status_code=404)

    def test_400_page_renders_custom_template(self):
        request = self.factory.get("/bad-request/")
        response = defaults.bad_request(request, Exception("bad request"))

        self.assertEqual(response.status_code, 400)
        self.assertIn("Некорректный запрос", response.content.decode())
        self.assertIn('class="error-panel__backdrop"', response.content.decode())
        self.assertNotIn('class="site-header"', response.content.decode())

    def test_403_page_renders_custom_template(self):
        request = self.factory.get("/forbidden/")
        response = defaults.permission_denied(request, Exception("forbidden"))

        self.assertEqual(response.status_code, 403)
        self.assertIn("Доступ запрещён", response.content.decode())
        self.assertIn('class="error-panel__backdrop"', response.content.decode())
        self.assertNotIn('class="site-header"', response.content.decode())

    def test_500_page_renders_custom_template(self):
        request = self.factory.get("/server-error/")
        response = defaults.server_error(request)

        self.assertEqual(response.status_code, 500)
        self.assertIn("Ошибка сервера", response.content.decode())
        self.assertIn('class="error-panel__backdrop"', response.content.decode())
        self.assertNotIn('class="site-header"', response.content.decode())
