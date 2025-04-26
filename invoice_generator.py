from datetime import datetime

def generate_invoice_html(data):
    """Generate HTML for the invoice based on provided data"""
    
    # Calculate tax and totals
    subtotal = sum(item["qty"] * item["price"] for item in data["items"])
    tax_rate = data["invoice"]["taxRate"]
    tax_amount = (subtotal * tax_rate) / 100
    total = subtotal + tax_amount
    advance_payment = data["invoice"]["advancePayment"]
    balance_due = max(0, total - advance_payment)
    
    # Format date
    try:
        date_obj = datetime.strptime(data["invoice"]["date"], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d-%m-%Y")
    except:
        formatted_date = data["invoice"]["date"]
    
    # Generate HTML (using the same template as in server.js)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Invoice</title>
        <style>
            body {{ 
                font-family: 'Montserrat', 'Poppins', 'Segoe UI', sans-serif;
                margin: 0;
                padding: 0;
                color: #333;
                line-height: 1.3;
                font-size: 14px;
            }}
            .blueside-invoice {{ max-width: 800px; margin: 0 auto; }}
            .blueside-header {{ 
                background-color: #2a4aa1;
                color: white;
                padding: 18px;
                display: flex;
                justify-content: space-between;
            }}
            /* ...existing CSS styles... */
        </style>
    </head>
    <body>
        <div class="blueside-invoice">
            <div class="blueside-header">
                <div class="blueside-header-left">
                    <img src="https://i.ibb.co/d0PF4sQg/Untitled-design-3.png" alt="Company Logo" style="max-width: 180px; height: auto; margin-bottom: 5px;">
                    <div>
                        <p class="company-name">{data["company"]["name"]}</p>
                        <p class="company-tagline">Your Premier Travel & Adventure Partner</p>
                    </div>
                </div>
                <div class="blueside-header-right">
                    <div class="invoice-from">
                        <h3 style="font-size: 0.75rem; margin: 0; color: #333;">Invoice From</h3>
                        <p style="font-size: 0.7rem; line-height: 1.2; margin: 2px 0;">{data["company"]["address"].replace("\n", "<br>")}</p>
                        <p style="font-size: 0.7rem; margin: 2px 0 0 0; color: #555;">Phone: {data["company"]["phone"]}</p>
                    </div>
                    <p style="margin: 0; font-size: 0.7rem; color: rgba(255,255,255,0.9);">Total Amount</p>
                    <p class="total-display">₹{total:.2f}</p>
                </div>
            </div>
            
            <div class="blueside-body">
                <!-- Client info section -->
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px; padding-bottom: 5px; border-bottom: 1px solid #eee;">
                    <div style="width: 60%;">
                        <h3 style="font-size: 0.85rem; margin: 0 0 3px 0;">Invoice To:</h3>
                        <p style="font-size: 0.9rem; margin: 0 0 1px 0;"><strong>{data["client"]["name"]}</strong></p>
                        <p style="white-space: pre-line; color: #555; font-size: 0.75rem; line-height: 1.2; margin: 0;">{data["client"]["address"]}</p>
                        {"<p style='color: #555; font-size: 0.75rem; margin: 1px 0 0 0;'>GSTIN: " + data["client"]["gst"] + "</p>" if data["client"].get("gst") else ""}
                    </div>
                    <div style="text-align: right; width: 35%;">
                        <p style="font-size: 0.75rem; margin: 0 0 2px 0;">Invoice #: <strong>{data["invoice"]["number"]}</strong></p>
                        <p style="font-size: 0.75rem; margin: 0 0 2px 0;">Date: <strong>{formatted_date}</strong></p>
                        <p style="font-size: 0.75rem; margin: 0;">GSTIN: <strong>{data["company"]["gst"]}</strong></p>
                    </div>
                </div>
                
                <!-- Items table -->
                <table style="margin-top: 5px; margin-bottom: 10px; width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr>
                            <th style="width: 25px; padding: 4px 6px; background-color: #f8f8f8; text-align: left; font-size: 0.75rem; color: #444;">#</th>
                            <th style="padding: 4px 6px; background-color: #f8f8f8; text-align: left; font-size: 0.75rem; color: #444;">Description</th>
                            <th style="width: 40px; padding: 4px 6px; background-color: #f8f8f8; text-align: left; font-size: 0.75rem; color: #444;">Qty</th>
                            <th style="width: 65px; padding: 4px 6px; background-color: #f8f8f8; text-align: left; font-size: 0.75rem; color: #444;">Price</th>
                            <th style="width: 70px; padding: 4px 6px; text-align: right; background-color: #f8f8f8; font-size: 0.75rem; color: #444;">Amount</th>
                        </tr>
                    </thead>
                    <tbody style="background-color: #212121; color: white;">
                        {"".join([f'''
                            <tr>
                                <td style="padding: 4px 6px; font-size: 0.8rem;">{str(idx + 1).zfill(2)}</td>
                                <td style="padding: 4px 6px; font-size: 0.8rem;">{item["name"]}</td>
                                <td style="padding: 4px 6px; font-size: 0.8rem;">{item["qty"]}</td>
                                <td style="padding: 4px 6px; font-size: 0.8rem;">₹{item["price"]:.2f}</td>
                                <td style="padding: 4px 6px; text-align: right; font-size: 0.8rem;">₹{item["qty"] * item["price"]:.2f}</td>
                            </tr>
                        ''' for idx, item in enumerate(data["items"])])}
                    </tbody>
                </table>
                
                <!-- Summary box -->
                <div class="summary-box" style="background-color: #f0f4ff; padding: 10px; border-radius: 6px; margin-bottom: 15px; font-size: 0.85rem;">
                    <div style="display: flex; justify-content: space-between;">
                        <span>Sub Total:</span>
                        <span>₹{subtotal:.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 4px;">
                        <span>GST ({tax_rate}%):</span>
                        <span>₹{tax_amount:.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 4px; padding-top: 4px; border-top: 1px solid rgba(0,0,0,0.1); font-weight: bold; font-size: 0.9rem;">
                        <span>Total:</span>
                        <span>₹{total:.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 4px; color: #4b5563;">
                        <span>Advance Payment:</span>
                        <span>₹{advance_payment:.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 4px; padding-top: 4px; border-top: 1px solid rgba(0,0,0,0.1); font-weight: bold; font-size: 0.9rem; color: #2a4aa1;">
                        <span>Balance Due:</span>
                        <span>₹{balance_due:.2f}</span>
                    </div>
                </div>
                
                <!-- Payment method and QR code -->
                <div style="display: flex; justify-content: space-between; margin-bottom: 15px; align-items: center;">
                    <div style="width: 48%;">
                        <h4 style="color: #2a4aa1; margin: 0 0 5px 0; font-size: 0.85rem;">Payment Method</h4>
                        <p style="font-size: 0.8rem; line-height: 1.3; margin: 0;">{data["bankDetails"].replace("\n", "<br>")}</p>
                    </div>
                    
                    <div style="width: 48%; text-align: right;">
                        <img src="https://i.ibb.co/r2WyrJkV/Whats-App-Image-2025-04-25-at-13-33-27.jpg" alt="UPI QR Code" style="width: 220px; height: auto; border-radius: 6px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                        <p style="text-align: center; font-size: 0.8rem; margin: 5px 0 0 0; font-weight: 500;">Scan to Pay</p>
                    </div>
                </div>
                
                <!-- Terms and conditions -->
                <div style="border-top: 1px solid #eee; border-bottom: 1px solid #eee; padding: 8px 0; margin-bottom: 15px; font-size: 0.8rem;">
                    <h4 style="color: #2a4aa1; margin: 0 0 5px 0; font-size: 0.85rem;">Terms and Conditions</h4>
                    <p>{data["notes"]}</p>
                </div>
                
                <!-- Footer with contact info -->
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #555; align-items: center;">
                    <div style="display: flex; gap: 15px;">
                        <div>
                            <div style="background-color: #2a4aa1; color: white; width: 16px; height: 16px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-right: 4px; font-size: 0.6rem;">@</div>
                            <span>{data["company"]["name"].lower().replace(" ", "")}@gmail.com</span>
                        </div>
                        <div>
                            <div style="background-color: #2a4aa1; color: white; width: 16px; height: 16px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-right: 4px; font-size: 0.6rem;">☏</div>
                            <span>{data["company"]["phone"]}</span>
                        </div>
                    </div>
                    
                    <div>
                        <span style="margin-right: 6px; font-size: 0.75rem;">Authorized Signature</span>
                        <img src="https://i.ibb.co/Y40ck28f/Whats-App-Image-2025-04-25-at-13-34-44.jpg" alt="Signature" style="width: 75px; height: auto; vertical-align: middle;">
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html
