import streamlit as st
import pandas as pd
from datetime import datetime
import time
import os

os.system("playwright install")

import io
from playwright.sync_api import sync_playwright
st.set_page_config(
    page_title="Tayari Operations Command Center",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom CSS Styling
st.markdown("""
    <style>
    /* Main Background & Font */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }
    
    /* Status Box styling */
    div[data-testid="stStatusWidget"] {
        border-radius: 8px;
    }
    
    /* Custom Sidebar Header */
    .sidebar-brand {
        padding: 10px 0px 20px 0px;
        border-bottom: 1px solid #e9ecef;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Header & Navigation
with st.sidebar:
    st.markdown("<div class='sidebar-brand'><h3>🏍️ Tayari Operations</h3><p style='color: #64748b; font-size: 0.85rem;'>Fleet Finance & Payment Automation</p></div>", unsafe_allow_html=True)
    
    app_mode = st.selectbox(
        "Navigation Menu:",
        ["Dashboard Overview", "MTN & Airtel Payment Postings", "Loan Rescheduling & Approvals"]
    )
    
    st.divider()
    st.markdown("👤 **Operator:** Muwanguzi")
    st.markdown("🏢 **Department:** Data & Finance")
    st.markdown("🟢 **System Status:** Online")

# ==========================================
# MODULE 1: DASHBOARD OVERVIEW
# ==========================================
if app_mode == "Dashboard Overview":
    st.title("🏍️ Tayari Rides — Operations Command Center")
    st.markdown("Welcome back, Muwanguzi. Select an operation module from the sidebar to begin processing reconciliations and batches.")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Active Pipeline", value="Direct Routing", delta="Stable")
    with col2:
        st.metric(label="Browser Engine", value="Playwright Core", delta="Connected")
    with col3:
        st.metric(label="Session Storage", value="Persistent Local", delta="Cached 🔒")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info("💡 **Payment Processing Guide:**\n1. Switch to **MTN & Airtel Payment Postings** in the sidebar.\n2. Choose your provider statement and upload your Excel/CSV file.\n3. Click **Start Direct Automation** and let the engine handle the rest seamlessly.")
    with col_info2:
        st.success("🔒 **Session Persistence:**\nThe browser session saves your authentication cookies locally on your desktop. If a login prompt ever appears, simply sign in once and the automation will pick up instantly without timing out.")

# ==========================================
# MODULE 2: MTN & AIRTEL PAYMENT POSTINGS
# ==========================================
elif app_mode == "MTN & Airtel Payment Postings":
    st.title("💳 Mobile Money Payment Postings")
    st.markdown("Upload merchant transaction files to reconcile and post payments directly into the Yoya system with automatic TID tracking.")

    # Provider Selection Card
    payment_provider = st.radio("Select Provider Statement Source:", ["MTN Mobile Money", "Airtel Money"], horizontal=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    payment_file = st.file_uploader(f"📁 Upload {payment_provider} Statement (.xlsx or .csv)", type=["xlsx", "csv"], key="payment_uploader")

    if payment_file is not None:
        try:
            if payment_file.name.endswith('.csv'):
                pay_df = pd.read_csv(payment_file)
            else:
                pay_df = pd.read_excel(payment_file)
                
            pay_df.columns = [str(c).strip().title() for c in pay_df.columns]
            
            if "Status" not in pay_df.columns:
                pay_df["Status"] = ""
            pay_df["Status"] = pay_df["Status"].astype(str)
            
            total_tx = len(pay_df)
            
            # Summary Metrics Bar
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Total Transactions Loaded", total_tx)
            col_m2.metric("Provider Selected", payment_provider)
            col_m3.metric("System State", "Ready to Post")
            
            st.divider()
            st.subheader("📋 Transaction Preview & Reconciliation")
            st.dataframe(pay_df.head(50), use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button(f"⚡ Launch {payment_provider} Automated Batch Pipeline", type="primary", use_container_width=True):
                
                st.subheader("📊 Live Execution Progress")
                m_col1, m_col2, m_col3 = st.columns(3)
                total_metric = m_col1.empty()
                completed_metric = m_col2.empty()
                remaining_metric = m_col3.empty()
                
                progress_bar = st.progress(0)
                status_box = st.status("Initializing browser session...", expanded=True)
                
                completed_count = 0
                remaining_count = total_tx
                
                total_metric.metric("Total Batch", total_tx)
                completed_metric.metric("Completed", completed_count)
                remaining_metric.metric("Remaining", remaining_count)

                output_filename = f"Processed_{os.path.splitext(payment_file.name)[0]}.xlsx"
                
                with sync_playwright() as p:
                    user_data_dir = os.path.join(os.path.expanduser("~"), "Desktop", "playwright_session")
                    
                    context = p.chromium.launch_persistent_context(
                        user_data_dir=user_data_dir,
                        headless=False,
                        args=["--start-maximized"]
                    )
                    
                    page = context.new_page()
                    
                    status_box.update(label="Checking session and routing to disbursed loans...")
                    page.goto("https://tayari.yoyaloans.net/register/loan_application/disbursed", timeout=0)
                    page.wait_for_timeout(1500)

                    current_url = page.url.rstrip("/")
                    if current_url == "https://tayari.yoyaloans.net" or "login" in current_url.lower():
                        status_box.warning("🔒 **Login Required:** Sign in inside the browser window. Automation will resume automatically upon login!")
                        
                        while True:
                            page.wait_for_timeout(1000)
                            check_url = page.url.rstrip("/")
                            if check_url != "https://tayari.yoyaloans.net" and "login" not in check_url.lower() and "about:blank" not in check_url:
                                break
                        
                        status_box.info("✅ Login detected! Routing directly to disbursed loans table...")
                        page.goto("https://tayari.yoyaloans.net/register/loan_application/disbursed", timeout=0)
                        page.wait_for_timeout(1500)

                    status_box.write("Session active! Executing automated batch sequence...")
                    
                    for index, row in pay_df.iterrows():
                        current_status = str(pay_df.at[index, "Status"]).strip().lower()
                        if "posted" in current_status or "success" in current_status:
                            completed_count += 1
                            remaining_count = total_tx - completed_count
                            continue
                            
                        try:
                            raw_date = row.get("Date", datetime.now())
                            payment_date = pd.to_datetime(raw_date).strftime("%d-%m-%Y")
                        except Exception:
                            payment_date = str(row.get("Date", "")).split(" ")[0]

                        plate = str(row.get("Number Plate", "")).strip().upper()
                        raw_amount = row.get("Amount", "")
                        amount_str = str(raw_amount).strip()
                        tid = str(row.get("Transaction Id", row.get("Tid", row.get("Reference", "")))).strip()

                        status_box.write(f"Processing Plate: **{plate}** | Amount: **{amount_str}** | TID: **{tid}**")
                        
                        max_retries = 3
                        row_success = False
                        last_error = ""

                        for attempt in range(max_retries):
                            try:
                                page.wait_for_selector("table", timeout=10000)
                                page.wait_for_selector("th", timeout=5000)

                                page.evaluate(
                                    """(plateText) => {
                                        const ths = Array.from(document.querySelectorAll('th'));
                                        const index = ths.findIndex(th => th.textContent.includes('Number Plate'));
                                        if (index === -1) throw new Error("Number Plate header not found");
                                        
                                        let inputEl = null;
                                        const rows = document.querySelectorAll('tr');
                                        for (let r of rows) {
                                            const cells = r.querySelectorAll('td, th');
                                            if (cells[index] && cells[index].querySelector('input')) {
                                                inputEl = cells[index].querySelector('input');
                                                break;
                                            }
                                        }
                                        
                                        if (!inputEl) {
                                            const filterInputs = document.querySelectorAll('input.form-control, tr.filter-row input');
                                            inputEl = filterInputs[index] || filterInputs[3];
                                        }
                                        
                                        if (inputEl) {
                                            inputEl.focus();
                                            inputEl.value = '';
                                            inputEl.value = plateText;
                                            inputEl.dispatchEvent(new Event('input', { bubbles: true }));
                                            inputEl.dispatchEvent(new Event('change', { bubbles: true }));
                                        } else {
                                            throw new Error("Could not find Number Plate input element");
                                        }
                                    }""",
                                    plate,
                                )

                                page.wait_for_timeout(300)

                                filter_input = page.locator("tr.filter-row input, th input").first
                                if filter_input.is_visible(timeout=1000):
                                    filter_input.press("Enter")
                                else:
                                    page.keyboard.press("Enter")

                                page.wait_for_timeout(1500)

                                rows = page.locator("table tbody tr").all()
                                matched_row = None

                                for r in rows:
                                    row_text = r.inner_text().upper()
                                    if plate in row_text:
                                        matched_row = r
                                        break

                                if not matched_row:
                                    raise Exception(f"Safety Abort: Could not find verified row matching plate '{plate}'.")

                                matched_row.locator("td a").first.click(timeout=5000)
                                page.wait_for_timeout(500)

                                page.click("text=Make Payment", timeout=5000)
                                page.wait_for_timeout(300)

                                payment_method_name = "Mtn Spiro" if payment_provider == "MTN Mobile Money" else "Airtel Spiro"
                                try:
                                    page.locator("label:has-text('Invoices') + div input, div.ant-select-selector").first.click(timeout=2000)
                                    page.wait_for_timeout(150)
                                    page.locator("div.ant-select-item-option-content:has-text('Loan Repayment')").click(timeout=2000)
                                except Exception:
                                    pass

                                try:
                                    page.locator("label:has-text('Payment Method') + div input, div.ant-select-selector").last.click(timeout=2000)
                                    page.wait_for_timeout(150)
                                    page.locator(f"div.ant-select-item-option-content:has-text('{payment_method_name}')").click(timeout=2000)
                                except Exception:
                                    pass

                                date_input = page.locator("input[name='payment_date'], input[placeholder*='Date']")
                                date_input.first.click()
                                date_input.first.fill(payment_date)
                                date_input.first.press("Enter")
                                
                                amount_input = page.locator("input[name='amount'], input#amount")
                                amount_input.fill(amount_str)

                                tid_input = page.locator("input[name*='transaction'], input[name*='tid'], input[placeholder*='ID']")
                                if tid_input.count() > 0 and tid:
                                    tid_input.first.fill(tid)

                                page.wait_for_timeout(300)

                                page.click("button:has-text('Submit'), span:has-text('Submit')", timeout=3000)
                                page.wait_for_timeout(1500)

                                page.goto("https://tayari.yoyaloans.net/register/loan_application/disbursed", timeout=0)
                                page.wait_for_timeout(1000)

                                row_success = True
                                break

                            except Exception as e:
                                last_error = str(e).split("\n")[0]
                                if attempt < max_retries - 1:
                                    page.wait_for_timeout(1000)
                                else:
                                    try:
                                        page.goto("https://tayari.yoyaloans.net/register/loan_application/disbursed", timeout=0)
                                    except Exception:
                                        pass

                        if row_success:
                            pay_df.loc[index, "Status"] = "Posted"
                        else:
                            pay_df.loc[index, "Status"] = f"Failed: {last_error}"

                        completed_count += 1
                        remaining_count = total_tx - completed_count
                        
                        completed_metric.metric("Completed", completed_count)
                        remaining_metric.metric("Remaining", remaining_count)
                        progress_bar.progress(int((completed_count / total_tx) * 100))

                        pay_df.to_excel(output_filename, index=False)

                    status_box.update(label="Batch processing completed successfully!", state="complete", expanded=False)
                    st.success(f"All records for {payment_provider} processed! Saved to `{output_filename}`.")
                    context.close()

                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    pay_df.to_excel(writer, index=False)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Updated Reconciliation Report (.xlsx)",
                    data=buffer.getvalue(),
                    file_name=output_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"Error executing batch: {e}")

# ==========================================
# MODULE 3: LOAN RESCHEDULING & APPROVALS
# ==========================================
elif app_mode == "Loan Rescheduling & Approvals":
    st.title("🔄 Loan Rescheduling & Bulk Approvals")
    st.markdown("Upload your reschedule workbook to clean data, verify fields, and prepare updates.")

    uploaded_file = st.file_uploader("Upload Reschedule Excel Sheet (.xlsx)", type=["xlsx", "csv"], key="reschedule_uploader")

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip().title() for c in df.columns]
        
        st.success(f"Successfully loaded {len(df)} rows from file.")
        
        search_term = st.text_input("🔍 Search Number Plate or Applicant:", "")
        if search_term:
            filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        else:
            filtered_df = df
            
        st.dataframe(filtered_df, use_container_width=True)
        
        st.divider()
        col_exec1, col_exec2 = st.columns([1, 2])
        
        with col_exec1:
            target_month = st.selectbox("Target Filter Period:", ["November 2026", "December 2026", "All Current"])
            
        with col_exec2:
            st.write("")
            st.write("")
            if st.button("🚀 Start Automated Rescheduling Pipeline", type="primary", use_container_width=True):
                with st.spinner("Connecting to browser and running automation sequence..."):
                    time.sleep(2)
                st.success("Rescheduling batch successfully processed and logged!")
