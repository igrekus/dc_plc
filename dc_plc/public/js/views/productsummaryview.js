export function view_test () {
    console.log(">>> custom js <<");
}


// frappe.provide('frappe.views');


// frappe.views.ReportView = class ReportView extends frappe.views.ListView {
//     // get view_name() {
//     //     return 'Product View';
//     // }
//     //
//     // setup_defaults() {
//     //     super.setup_defaults();
//     //     this.page_title = __('Product View:') + ' ' + this.page_title;
//     //     this.menu_items = this.report_menu_items();
//     //
//     //     const route = frappe.get_route();
//     //     if (route.length === 4) {
//     //         this.report_name = route[3];
//     //     }
//     //
//     //     this.add_totals_row = this.view_user_settings.add_totals_row || 0;
//     //
//     //     if (this.report_name) {
//     //         return this.get_report_doc()
//     //             .then(doc => {
//     //                 this.report_doc = doc;
//     //                 this.report_doc.json = JSON.parse(this.report_doc.json);
//     //
//     //                 this.filters = this.report_doc.json.filters;
//     //                 this.order_by = this.report_doc.json.order_by;
//     //                 this.add_totals_row = this.report_doc.json.add_totals_row;
//     //                 this.page_title = this.report_name;
//     //                 this.page_length = this.report_doc.json.page_length || 20;
//     //                 this.order_by = this.report_doc.json.order_by || 'modified desc';
//     //             });
//     //     }
//     // }
// };
