
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from oauth2_provider.models import Application
from users.models import User
import tempfile
from song.models import Music, UniqueCode
from rest_framework.utils import json
from django.core.files.uploadedfile import SimpleUploadedFile
from daraja.models import Payment, TransStatus, TransReversal, LipaNaMpesa, \
    SuccessTransaction, B2cPayment


class BaseAPITest(APITestCase):
    username = "admin@bittcash.org"
    username2 = "kelvinmutea@gmail.com"
    password = "admin123"
    client_id = "iuyutyutuyctua"
    client_secret = "lahkckagkegigciegvjegvjhv"
    phone_number = '0712021679'
    #Daraja stuff
    CheckoutRequestID = 'ws_CO_04112017184930742'
    OriginatorConversationID = "14593-80515-2"
    data = {'order_number': '100', 'PhoneNumber': '254712021679',
                 'amount': 2000.0, 'type': 'D', 'TransactionID': 'LK451H35OP',
                 'CheckoutRequestID': 'ws_CO_04112017184930742'}

    def setUp(self):
        user = User.objects.create(username=self.username2, role="A", phone_number="254712021679",
                                   email=self.username2, nick_name="Kigush")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.user = user
        self.user.set_password(self.password)
        self.user.save()
        # daraja setup tests
        Payment.objects.create(**self.data)
        LipaNaMpesa.objects.create(payment_id=1, CheckoutRequestID=self.CheckoutRequestID)
        # B2cPayment.objects.create(payment_id=1, OriginatorConversationID=self.OriginatorConversationID)

        # Setting django oauth2 application
        self.cl = APIClient()
        app = Application()
        app.client_id = self.client_id
        app.user = self.user
        app.authorization_grant_type = "password"
        app.client_type = "public"
        app.client_secret = self.client_secret
        app.save()

        # Create a hospital staff Staff Amdin #user id 2
        # resp = self.create_user()
        # print("The resp create user is", resp.json())
        # self.assertEqual(resp.status_code, 201)
        # Requesting token for a user
        self.get_token()
        self.user_authenticate()
        music = self.create_music()
        # print("The music response is", music.data)

    # Creating another second user
    def create_user(self, data=None):
        user_data = {"first_name": "Test", "last_name": "Doe",
                     "password": "bittcash", "email": self.username,
                     "phone_number": "254722021679", 'invitation_code': ''}
        if data is None:
            data = user_data
        url = reverse("list_register_user")
        return self.client.post(url, data)

    # Requesting for token
    def get_token(self, username="kelvinmutea@gmail.com", password="admin123"):
        user = "username={}&password={}&client_id={}&grant_type=password".format(username, password, self.client_id)
        url = "/o/token/"
        return self.client.post(url, user, content_type="application/x-www-form-urlencoded")

    # User authentication
    def user_authenticate(self, data=None):
        user_data = {"username": "kelvinmutea@gmail.com", "password": "admin123"}
        if data is None:
            data = user_data
        self.client.login(**data)

    # daraja payment stuff
    def url_registration(self):
        url = reverse('register_url')
        data = {'response_type': 'Completed'}
        return self.client.post(url, data)

    def complete_stk_response(self):
        url = reverse('stk_push')
        data = open('stk-res.json', 'r')
        data = json.load(data)
        return self.client.post(url, data, format='json')

    def overpaid_stk_response(self):
        url = reverse('stk_push')
        data = open('stk-res-overpaid.json', 'r')
        data = json.load(data)
        return self.client.post(url, data, format='json')

    def underpaid_stk_response(self):
        url = reverse('stk_push')
        data = open('stk-res-underpaid.json', 'r')
        data = json.load(data)
        return self.client.post(url, data, format='json')

    def status_response(self):
        url = reverse('trans_status')
        data = open('trans_status.json', 'r')
        data = json.load(data)
        return self.client.post(url, data, format='json')

    def b2c_response(self):
        url = reverse('b2c-response')
        data = open('b2c_response.json', 'r')
        data = json.load(data)
        return self.client.post(url, data, format='json')

    def balance_response(self):
        url = reverse('balance')
        data = open('balance_response.json', 'r')
        data = json.load(data)
        return self.client.post(url, data, format='json')

    # The tests on the developer side
    def payment_creation(self):
        url = reverse('pay')
        data = {'order_number': 1, 'phone': '0728922269', 'amount': 1, 'type': 'D'}
        return self.client.post(url, data)

    def status_enquiry(self):
        url = reverse('status')
        data = {'transaction_id': 133}
        return self.client.post(url, data)

    def reversal(self):
        url = reverse('reversal')
        data = {'transaction_id': 133}
        return self.client.post(url, data)

    def balance_enquiry(self):
        url = reverse('test_balance')
        data = {"get_balance": True}
        return self.client.post(url, data)

    # def balance_response(self):
    #     url = reverse('balance')
    #     data = open('balance_response.json', 'r')
    #     data = json.load(data)
    #     return self.client.post(url, data, format='json')

    def create_music(self, data=None):
        url = reverse('music_upload_list')
        music_file = SimpleUploadedFile("basetest.mp3", b"this is the file", content_type="audio/mpeg")
        if data is None:
            data = {'music_file': music_file, 'song_name': 'Aluta', 'price': 20, 'custom_link': 'Ochunglo fam'}
        # print("The data for music creation is", data)
        return self.client.post(url, data)
