from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.guest_client = Client()
        cls.user = User.objects.create(username='test_user')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.user_not_author = User.objects.create(username='NotAuthor')
        cls.authorized_not_author_client = Client()
        cls.authorized_not_author_client.force_login(cls.user_not_author)

        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовый текст',
            slug='test_slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост'
        )

    def setUp(self):
        pass

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_url_exists_at_desired_location(self):
        """Страница /group/<slug>/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test_slug/')
        self.assertEqual(response.status_code, 200)

    def test_profile_exists_at_desired_location(self):
        """Страница /profile/<username>/ доступна любому пользователю."""
        response = self.guest_client.get('/profile/test_user/')
        self.assertEqual(response.status_code, 200)

    def test_posts_id_url_exists_at_desired_location_authorized(self):
        """Страница /posts/<post_id>/ доступна любому пользователю."""
        response = self.guest_client.get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_url_exists_at_desired_location(self):
        """Страница /create/ доступна только для
        авторизованных пользователей."""
        response_authorized = self.authorized_client.get('/create/')
        response_not_authorized = self.guest_client.get('/create/')
        self.assertEqual(response_authorized.status_code, 200)
        self.assertEqual(response_not_authorized.status_code, 302)

    def test_post_edit_avalible_only_for_author(self):
        """Страница /posts/post.id/edit/ доступна только автору"""
        response_authorized = self.authorized_client.get(
            f'/posts/{self.post.id}/edit/')
        response_not_authorized = self.guest_client.get(
            f'/posts/{self.post.id}/edit/')
        response_not_author = self.authorized_not_author_client.get(
            f'/posts/{self.post.id}/edit/')

        self.assertEqual(response_authorized.status_code, 200)
        self.assertEqual(response_not_authorized.status_code, 302)
        self.assertEqual(response_not_author.status_code, 302)

    def test_404_url_exists_at_desired_location(self):
        """Страница /404/ доступна любому пользователю."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test_slug/': 'posts/group_list.html',
            '/profile/test_user/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/create.html',
            '/create/': 'posts/create.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
