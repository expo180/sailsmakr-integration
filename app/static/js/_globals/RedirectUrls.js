const BaseURL = 'https://afrilog.onrender.com/';

const RedirectURLs = {
    LoginSuccessRedirectURL: `${BaseURL}home`,
    SignupSuccessRedirectURL: `${BaseURL}auth/login`,
    NoteCreationSuccessURL: `${BaseURL}notes/previous_notes`,
    JobCreationSuccessURL: `${BaseURL}careers/previous_created_jobs`,
    EmployeeEditInfoSuccess: `${BaseURL}careers/employees_table`,
    CreateAdSuccessURL: `${BaseURL}ads/`,
    PurchaseRequestSendSuccess: `${BaseURL}my_purchases/previous_purchase_requests`,
    AuthorizationSuccessRedirectURL: `${BaseURL}quotes/previouses`,
    ApplyJobSuccessRedirectURL: `${BaseURL}my-previous-applications`
};

export default RedirectURLs;
