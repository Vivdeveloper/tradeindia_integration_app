// Copyright (c) 2024, sushant and contributors
// For license information, please see license.txt

frappe.ui.form.on('TradeIndia API settings', {
    refresh: function (frm) {
        // Add a custom button
        frm.add_custom_button(__('Fetch Data'), function () {
            // Call the server-side method
            frappe.call({
                method: 'tradeindia_integration.tradeindia.doctype.tradeindia_api_settings.tradeindia_api_settings.fetch_tradeindia_data',
                callback: function (r) {
                    if (r.message) {
                        frappe.msgprint(__('Fetched Date: {0}', [r.message]));
                    }
                }
            });
        });
    }
});
