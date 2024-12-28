# Copyright (c) 2024, sushant and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

import requests
import frappe
from frappe.utils import now, today, add_days


class TradeIndiaAPIsettings(Document):
	pass

@frappe.whitelist()
def fetch_tradeindia_data():
	
	settings = frappe.get_single("TradeIndia API settings")
	if not settings:
		frappe.log_error("TradeIndia API Settings doctype not found", "TradeIndia Integration")
		return
	
	user_id = settings.user_id
	profile_id = settings.profile_id
	key = settings.key
	from_date =  today()
	to_date =  today()
	limit =  100
	page_no =  1
	
	url = f"https://www.tradeindia.com/utils/my_inquiry.html?userid={user_id}&profile_id={profile_id}&key={key}&from_date={from_date}&to_date={to_date}&limit={limit}&page_no={page_no}"
	
	try:
		response = requests.get(url)
		response.raise_for_status()
		data = response.json()
		print(url)
		
		if isinstance(data, list):
			for record in data:
				rfi_id = record.get("rfi_id")
				if not frappe.db.exists("TradeIndia Lead", {"query_id": rfi_id}):
					doc = frappe.new_doc("TradeIndia Lead")
					doc.query_id = rfi_id
					doc.tradeindia_lead_data = record
					doc.status = "Queued"
					doc.created_on = now()
					doc.insert()
				else:
					print(f"Duplicate entry found for rfi_id: {rfi_id}")
		else:
			frappe.log_error("Unexpected data format from TradeIndia API", "TradeIndia Integration")
	except requests.exceptions.RequestException as e:
		frappe.log_error(f"RequestException: {str(e)}", "TradeIndia API Fetch Error")
	except Exception as e:
		frappe.log_error(f"Unexpected error: {str(e)}", "TradeIndia API Error")
    