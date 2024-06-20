const BaseURL = 'https://afrilog.onrender.com/api/v1/';
const SecBaseURL = 'https://afrilog.onrender.com/';

const UtilApiURLs = {
    GetEventsApiURL: `${BaseURL}get_events`,
    ManageTaskURL: `${BaseURL}manage/task/`,
    ManageNoteURL: `${BaseURL}manage/note/`,
    DeleteEmployeeURL: `${BaseURL}careers/employees/delete_employee/`,
    DeleteAdURL: `${BaseURL}ads/delete_ad/`,
    DeletePurchaseRequestURL: `${BaseURL}my_purchases/delete/`,
    PopulatePurchaseDataListURL: `${BaseURL}my_purchases/track_my_product/user`,
    DeleteAuthorizationRequestURL: `${BaseURL}delete_request/`,
    DeletePurchaseRequestURLSales: `${BaseURL}delete_purchase/`,
    EditInvoiceRequestURL: `${BaseURL}edit_invoice/`,
    DeleteInvoiceRequestURL: `${BaseURL}delete_invoice/`,
    checkValidityQuoteURL: `${BaseURL}quote/edit/`,
    DeleteQuoteRequestURL: `${BaseURL}quote/delete/`,
    AddressAutoCompleteURL: `${BaseURL}autocomplete-address`,
    GetAirFreightRatesURL : `${BaseURL}get-air-freight-rate`,
    GetRealTimeWeatherURL : `${BaseURL}get-weather/realtime`,
    AddStoreURL: `${BaseURL}add_store`,
    EditStoreURL: `${BaseURL}edit_store/`,
    DeleteStoreURL: `${BaseURL}delete_store/`,
    ApplyJobURL: `${BaseURL}job-openings/apply/`,
    DeleteStoreURL : `${SecBaseURL}stores`,
    EditStoreURL : `${SecBaseURL}stores`,
    GetStoreDetailsURL : `${BaseURL}get-store_details/`,
    ManageProductURL: `${SecBaseURL}products`,
    GetProductBarCodeURL : `${BaseURL}download_barcode/`,
    SendQuoteRequestURL : `${BaseURL}send-message`,
    SendWhatsappMassageURL : `${BaseURL}send-whatsapp-message`
};

export default UtilApiURLs;
