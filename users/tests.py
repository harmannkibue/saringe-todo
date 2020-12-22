from mylib.tests import BaseAPITest
from rest_framework.reverse import reverse
from .models import User
from datetime import datetime
# from django.core import mail
import pytz

utc = pytz.UTC


# Create your tests here.
class UserTests(BaseAPITest):

    # Requesting token
    def test_token_generation(self):
        resp = self.get_token()
        # print(resp.json())
        self.assertEqual(resp.status_code, 200)

    # User login
    def test_login_user(self):
        resp = self.get_token()
        # print("The value of resp is", resp.json())
        token = resp.json()["access_token"]
        # print("The token is", token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % (token))
        resp = self.client.get(reverse("user_profile"))
        # print(resp.json())
        self.assertEqual(resp.status_code, 200)

    def test_user_creation(self):
        user_data = {"first_name": "john", "last_name": "kamaru",
                     "password": "bittcash", "email": "papakamaru@gmail.com",
                     "phone_number": "254742021679", "nick_name": "Omollo"}
        resp = self.create_user(user_data)
        self.assertEqual(resp.status_code, 201)

    # Changing password with wrong password
    def test_change_password_wrong_password(self):
        self.user_authenticate()
        data = {"old_password": "wrongpass", "new_password": "bitcoin"}
        resp = self.client.put(reverse("change_password"), data)
        # print("The resp password", resp.data)
        self.assertEqual(resp.data, {'old_password': ['Wrong password.']})
        self.assertEquals(resp.status_code, 400)

    # Changing password with correct password
    def test_change_password_correct_password(self):
        self.user_authenticate()
        data = {"old_password": "admin123", "new_password": "newpass"}
        resp = self.client.put(reverse("change_password"), data)
        # print("The password ", resp.json())
        self.assertEqual(resp.data["detail"], "Password successfully changed.")
        self.assertEquals(resp.status_code, 200)

    # Testing sending password reset code with correct email
    # def test_forgot_password_correct_email(self):
    #     data = {"email": "kelvinmutea@gmail.com"}
    #     User.objects.filter(email="kelvinmutea@gmail.com").update(reset_code=9999)
    #     resp = self.client.post(reverse("forgot_password"), data)
    #     # print("The response at forgot password correct email", resp.data)
    #     self.assertEqual(resp.data["detail"], 'Reset code sent successfully to kelvinmutea@gmail.com.')
    #     self.assertEqual(resp.status_code, 200)

    # Testing forgot code with wrong email
    # def test_forgot_password_wrong_email(self):
    #     data = {"email": "jaahzino@gmail.com"}
    #     resp = self.client.post(reverse("forgot_password"), data)
    #     print(resp.data)
    #     self.assertEqual(resp.status_code, 400)

    # Testing reset password with code
    # def test_resetting_password(self):
    #     User.objects.filter(username="kelvinmutea@gmail.com").update(reset_code=9999)
    #     new_password = "newpassword"
    #     username = "kelvinmutea@gmail.com"
    #     time_code_created = datetime.now().replace(tzinfo=utc)
    #     user = User.objects.get(username=username)
    #     user.time_code_created = time_code_created
    #     user.save(update_fields=['time_code_created'])
    #     reset_code = user.reset_code
    #     data = {"new_password": new_password, "reset_code": reset_code}
    #     resp = self.client.post(reverse("reset_password"), data)
    #     self.assertEqual(resp.status_code, 200)

    # Testing requesting code
    # def test_requesting_code(self):
    #     data = {"username": "kelvinmutea@gmail.com"}
    #     resp = self.client.post(reverse("request_code"), data)
    #     print("The response in requesting code is", resp.json())
    #     self.assertEqual(resp.status_code, 200)

    def test_url_registration(self):
        res = self.url_registration()
        # print("The response in url registration is", res)
        self.assertEqual(res.status_code, 200)

    def test_complete_stk_response(self):
        res = self.complete_stk_response()
        # print("The res in stkresponse", res)
        self.assertEqual(res.status_code, 201)

    def test_overpaid_stk_response(self):
        res = self.overpaid_stk_response()
        # print("The res in stkresponse", res)
        # self.assertEqual(res.status_code, 201)

    def test_underpaid_stk_response(self):
        res = self.underpaid_stk_response()
        # print("The res in stkresponse", res)
        self.assertEqual(res.status_code, 201)

    def test_status_response(self):
        res = self.status_response()
        self.assertEqual(res.status_code, 200)

    # def test_b2c_response(self):
    #     res = self.b2c_response()
    #     # print("The b2c response is", res)
    #     self.assertEqual(res.status_code, 201)

    def test_balance_response(self):
        res = self.balance_response()
        self.assertEqual(res.status_code, 200)
