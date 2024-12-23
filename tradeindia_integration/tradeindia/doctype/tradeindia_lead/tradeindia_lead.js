// Copyright (c) 2024, sushant and contributors
// For license information, please see license.txt

frappe.ui.form.on("TradeIndia Lead", {
	refresh: function (frm) {
        if (!frm.doc.output) {
            frm.add_custom_button(__('Create Lead'), function() {
                frappe.call({
                    method: 'tradeindia_integration.tradeindia.doctype.tradeindia_lead.tradeindia_lead.fetch_tradeindia_data',
                    args: {
                        tradeindia_lead_name: frm.doc.name
                    },
                    callback: function(response) {
                        if (response.message) {
                            frappe.msgprint(response.message);
                            frm.reload_doc();
                        }
                    }
                });
            });
        } else {
            frm.add_custom_button(__('View Lead'), function() {
                frappe.set_route('Form', 'Lead', frm.doc.output);
            });
        }
    }
});
