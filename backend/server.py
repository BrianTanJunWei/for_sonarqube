from app.config.config import app
from flask_restful import Api
from app.api.api_user_login import LoginAPI
from app.api.api_admin_login import AdminLoginAPI
from app.api.api_logout import LogoutAPI
from app.api.api_profile import ProfileAPI,UpdateProfileAPI,CheckPhoneNumberExistsAPI
from app.api.api_security import ChangePasswordAPI, GenerateSessionTokenAPI, ForgotPasswordAPI
from app.api.api_profile import ProfileAPI,UpdateProfileAPI
from app.api.api_security import ChangePasswordAPI, GenerateSessionTokenAPI, ForgotPasswordAPI ,GetCurrentSessionTokenAPI, VerifyCaptchaAPI, GetUriAPI, Verify2FAAPI
from app.api.api_register import RegisterAPI , DeleteUserAPI
from app.api.api_seller_page import SellerProductsAPI,AddProductAPI,DeleteProductAPI,GetProductAPI,EditProductAPI,NotificationsAPI, DeleteNotificationAPI
from app.api.api_admin_console import GetAccountsAPI, UpdateUserStatusAPI, LoginLogsAPI, TransactionLogsAPI
from app.api.api_buyer_page import FetchAllProductsAPI, FetchFilteredProductsAPI
from app.api.api_cart import GetCartAPI, DeleteFromCartAPI, AddToCartAPI, CheckoutCartAPI

api = Api(app)

# Register API Resources
api.add_resource(LoginAPI, '/login')
api.add_resource(DeleteUserAPI, '/delete')
api.add_resource(GetCurrentSessionTokenAPI, '/verify-session-token')
api.add_resource(LogoutAPI, '/logout')
api.add_resource(AdminLoginAPI, '/AdminLogin')
api.add_resource(ProfileAPI, '/profile')
api.add_resource(UpdateProfileAPI, '/updateProfile')
api.add_resource(CheckPhoneNumberExistsAPI, '/checkPhoneNumberExists')
api.add_resource(GenerateSessionTokenAPI, '/generate-session-token')
api.add_resource(ChangePasswordAPI, '/change_password')
api.add_resource(ForgotPasswordAPI, '/forgot-password')
api.add_resource(RegisterAPI, '/register')
api.add_resource(SellerProductsAPI, '/Sellerproducts')
api.add_resource(DeleteProductAPI, '/delete-product/<string:productId>')
api.add_resource(GetProductAPI, '/get-product/<productID>')
api.add_resource(EditProductAPI, '/edit-product/<string:productID>')
api.add_resource(AddProductAPI, '/add-product')
api.add_resource(NotificationsAPI, '/get_notifications')
api.add_resource(DeleteNotificationAPI, '/delete-notification/<string:userId>/<string:notificationId>')
api.add_resource(GetAccountsAPI, '/get_accounts')
api.add_resource(UpdateUserStatusAPI, '/update_user_status')
api.add_resource(LoginLogsAPI, '/login_logs')
api.add_resource(TransactionLogsAPI, '/transaction_logs')
api.add_resource(FetchAllProductsAPI, '/FetchAllProducts')
api.add_resource(FetchFilteredProductsAPI, '/FetchFilteredProducts/<string:producttype>')
api.add_resource(GetCartAPI, '/get-cart/<userID>')
api.add_resource(AddToCartAPI, '/add-to-cart/<string:userId>/<string:productId>')
api.add_resource(DeleteFromCartAPI, '/delete-from-cart/<string:userId>/<string:productId>')
api.add_resource(CheckoutCartAPI, '/checkout/<string:userId>')
api.add_resource(VerifyCaptchaAPI, '/verify-recaptcha')
api.add_resource(GetUriAPI, '/getURI')
api.add_resource(Verify2FAAPI, '/verify2FA')

# Running app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
