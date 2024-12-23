# Copyright (c) 2024, sushant and contributors
# For license information, please see license.txt

# import frappe
import json
import frappe
from frappe.model.document import Document


class TradeIndiaLead(Document):
	pass


@frappe.whitelist()
def fetch_tradeindia_data(tradeindia_lead_name):
	print("success")
	try:
		tradeindia_lead = frappe.get_doc("TradeIndia Lead", tradeindia_lead_name)
	except frappe.DoesNotExistError:
		frappe.throw(f"TradeIndia Lead {tradeindia_lead_name} does not exist.")

	
	tradeindia_lead_data = tradeindia_lead.tradeindia_lead_data
	if not tradeindia_lead_data:
		frappe.throw("No data found in tradeindia_lead_data.")

	try:
		tradeindia_lead_data = json.loads(tradeindia_lead_data)
	except json.JSONDecodeError:
		frappe.throw("Invalid JSON format in tradeindia_lead_data")
	
	lead_name = tradeindia_lead_data.get("sender_name") 
	phone = tradeindia_lead_data.get("sender_mobile")
	email = tradeindia_lead_data.get("sender_email")  
	company_name = tradeindia_lead_data.get("sender_co")  
	subject = tradeindia_lead_data.get("subject") 
	message = tradeindia_lead_data.get("message") 
	inquiry_type = tradeindia_lead_data.get("inquiry_type")  
	sender_city = tradeindia_lead_data.get("sender_city")  
	sender_state = tradeindia_lead_data.get("sender_state")  
	sender_country = tradeindia_lead_data.get("sender_country") 

	if frappe.db.exists("Lead", {"email_id": email, "phone": phone}):
		frappe.msgprint(f"Lead with phone {phone} already exists.")
		return
	
	lead = frappe.new_doc("Lead")
	lead.lead_name = lead_name or "Unknown Lead"
	lead.email_id = email
	lead.phone = phone
	lead.company_name = company_name
	lead.job_title = subject
	# lead.notes = message
	# lead.source = "TradeIndia"
	lead.city = sender_city
	lead.state = sender_state
	
	# lead.inquiry_type = inquiry_type
	lead.insert(ignore_permissions=True)
	frappe.db.commit()

	tradeindia_lead.db_set("output", lead.name)
	tradeindia_lead.db_set("status", "Completed")
	frappe.msgprint(f"Lead {lead.name} created successfully.")

   
@frappe.whitelist()	
def process_tradeindia_leads():
    """Processes all TradeIndia Lead entries that are not completed."""
    leads_to_process = frappe.get_all(
        "TradeIndia Lead",
        filters={"status": ["!=", "Completed"]},
        fields=["name", "tradeindia_lead_data"]
    )

    for lead in leads_to_process:
        tradeindia_lead_name = lead.get("name")
        tradeindia_lead_data = lead.get("tradeindia_lead_data")

        try:
            if not tradeindia_lead_data:
                frappe.db.set_value("TradeIndia Lead", tradeindia_lead_name, "status", "No Data")
                frappe.msgprint(f"No data found for TradeIndia Lead {tradeindia_lead_name}")
                continue

            tradeindia_lead_data = json.loads(tradeindia_lead_data)
            lead_name = tradeindia_lead_data.get("sender_name")
            phone = tradeindia_lead_data.get("sender_mobile")
            email = tradeindia_lead_data.get("sender_email")
            company_name = tradeindia_lead_data.get("sender_co")
            subject = tradeindia_lead_data.get("subject")
            message = tradeindia_lead_data.get("message")
            inquiry_type = tradeindia_lead_data.get("inquiry_type")
            sender_city = tradeindia_lead_data.get("sender_city")
            sender_state = tradeindia_lead_data.get("sender_state")

            if frappe.db.exists("Lead", {"email_id": email, "phone": phone}):
                # frappe.db.set_value("TradeIndia Lead", tradeindia_lead_name, "status", "Duplicate")
                frappe.msgprint(f"Lead with phone {phone} already exists.")
                continue

            lead = frappe.new_doc("Lead")
            lead.lead_name = lead_name or "Unknown Lead"
            lead.email_id = email
            lead.phone = phone
            lead.company_name = company_name
            # lead.job_title = subject
            lead.city = sender_city
            lead.state = sender_state
            lead.insert(ignore_permissions=True)

            frappe.db.set_value("TradeIndia Lead", tradeindia_lead_name, "output", lead.name)
            frappe.db.set_value("TradeIndia Lead", tradeindia_lead_name, "status", "Completed")
            frappe.msgprint(f"Lead {lead.name} created successfully for TradeIndia Lead {tradeindia_lead_name}.")

        except json.JSONDecodeError:
            frappe.db.set_value("TradeIndia Lead", tradeindia_lead_name, "status", "Failed")
            frappe.msgprint(f"Invalid JSON format for TradeIndia Lead {tradeindia_lead_name}")

        except Exception as e:
            frappe.db.set_value("TradeIndia Lead", tradeindia_lead_name, "status", "Failed")
            frappe.log_error(f"Error processing TradeIndia Lead {tradeindia_lead_name}: {str(e)}", "TradeIndia Lead Processing Error")
