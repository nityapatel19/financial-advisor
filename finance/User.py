import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import base64
from Exceptions import *
import pickle


def load_users():
    with open("users.pkl", 'rb') as f:
        users = pickle.load(f)
    return users


def update_users(users):
    with open("users.pkl", 'wb') as f:
        pickle.dump(users, f)


class User:
    def __init__(self, name: str, email: str, dob: str, mobile: str, pan: str, ihs: int):
        try:
            if get_user_by_name(name):
                raise UserAlreadyExists
        except UserNotFound:
            pass

        self.name = name

        self.email = email
        self.dob = dob

        if len(pan) != 10:
            raise InvalidMobile

        self.mobile = mobile

        if len(pan) != 10:
            raise InvalidPAN

        self.pan = pan
        self.in_hand_salary = ihs
        self.nonce = ""
        self.password = ""
        self.account_ready = False

    def create_account(self, encrypted_password):
        decrypt_and_store_pass(encrypted_password, self)

    def authenticate(self, encrypted_password):
        pass_given = decrypt_pass(encrypted_password, self)
        if pass_given == self.password:
            return True

    def auth_by_dob(self, dob):
        if self.dob == dob:
            return True


class Rate:
    annual_rate = 10
    job_change_increase = 30
    inflation_rate = 6
    investment_return_rate = 12

    def __init__(self, annual_rate=10, job_change_increase=30, inflation_rate=6, investment_return_rate=12):
        self.annual_rate = annual_rate
        self.job_change_increase = job_change_increase
        self.inflation_rate = inflation_rate
        self.investment_return_rate = investment_return_rate


def send_nonce(user: User):
    user.nonce = str(random.randint(10 ** 31, (10 ** 32) - 1))
    return user.nonce


def encrypt_login(password: str, user: User):
    cipher = AES.new(user.nonce.encode(), AES.MODE_ECB)
    encoded_pass = base64.b64encode(cipher.encrypt(pad(password.encode(), 32)))
    return encoded_pass.decode()


def decrypt_and_store_pass(encrypted_login: str, user: User):
    cipher = AES.new(user.nonce.encode(), AES.MODE_ECB)
    decoded_login = cipher.decrypt(base64.b64decode(encrypted_login.encode()))
    user.password = hashlib.sha256(unpad(decoded_login, 32)).hexdigest()
    user.nonce = ""
    user.account_ready = True


def decrypt_pass(encrypted_login: str, user: User):
    cipher = AES.new(user.nonce.encode(), AES.MODE_ECB)
    decoded_login = cipher.decrypt(base64.b64decode(encrypted_login.encode()))
    user.nonce = ""
    return hashlib.sha256(unpad(decoded_login, 32)).hexdigest()


def add_user(user: User, password: str):
    users = load_users()
    users.append(user)
    send_nonce(user)
    encry = encrypt_login(password, user)
    user.create_account(encry)

    print(f"User {user.name} created")
    update_users(users)

    return user


def get_user_by_name(name: str):
    users = load_users()
    for user in users:
        if user.name == name:
            return user
    raise UserNotFound


def get_user(email: str, password: str):
    users = load_users()
    for user in users:
        if user.email == email:
            send_nonce(user)
            if user.authenticate(encrypt_login(password, user)):
                return user
            raise WrongPassword
    raise UserNotFound


def get_user_by_pan(pan: str, dob: str):
    users = load_users()
    for user in users:
        if user.pan == pan:
            if user.auth_by_dob(dob):
                return user
            raise InvalidDOB
    raise UserNotFound


if __name__ == '__main__':
    email = "ksjfec@kjsgn.com"
    name = "fcersfvcs"
    dob = "12/12/12"
    mobile = "1234567890"
    pan = "1234567890"
    ins = 360000

    password = "12345678"

    user = User(name, email, dob, mobile, pan, ins)
    add_user(user, password)

    print(get_user(email, password).name)
