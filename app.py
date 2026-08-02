from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

app = Flask(__name__)
app.secret_key = 'as_mohammad_master_peanut_key'

# --- डेटाबेस सेटअप ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///peanut_master_business.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'Income' या 'Expense'
    party_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(100), default="")
    amount = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '').strip()
    filter_type = request.args.get('filter_type', 'All')

    query = Transaction.query

    # सर्च फिल्टर (Party Name या Date के आधार पर)
    if search_query:
        query = query.filter(
            (Transaction.party_name.ilike(f'%{search_query}%')) | 
            (Transaction.date.ilike(f'%{search_query}%'))
        )

    # ड्रॉपडाउन टाइप फिल्टर
    if filter_type == 'Income':
        query = query.filter_by(type='Income')
    elif filter_type == 'Expense':
        query = query.filter_by(type='Expense')

    transactions = query.order_by(Transaction.id.desc()).all()
    
    # कुल कैलकुलेशन के लिए सभी रिकॉर्ड्स
    all_transactions = Transaction.query.all()
    total_income = sum(t.amount for t in all_transactions if t.type == 'Income')
    total_expense = sum(t.amount for t in all_transactions if t.type == 'Expense')
    net_balance = total_income - total_expense

    return render_template('index.html', 
                           transactions=transactions,
                           total_income=total_income, 
                           total_expense=total_expense, 
                           net_balance=net_balance,
                           search_query=search_query,
                           filter_type=filter_type)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'asmohammad786':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'गलत यूजरनेम या पासवर्ड!'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_t = Transaction(
            date=request.form['date'],
            type=request.form['type'],
            party_name=request.form['party_name'],
            quantity=request.form['quantity'],
            amount=float(request.form['amount'])
        )
        db.session.add(new_t)
        db.session.commit()
        return redirect(url_for('index'))
        
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    item = Transaction.query.get_or_404(id)
    if request.method == 'POST':
        item.date = request.form['date']
        item.type = request.form['type']
        item.party_name = request.form['party_name']
        item.quantity = request.form['quantity']
        item.amount = float(request.form['amount'])
        db.session.commit()
        return redirect(url_for('index'))
        
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete_transaction(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    item = Transaction.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    Transaction.query.delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/download_pdf')
def download_pdf():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#0f172a'),
        alignment=1,
        spaceAfter=15
    )
    
    elements.append(Paragraph("<b>As Mohammad Peanut Business - Master Ledger Report</b>", title_style))
    elements.append(Spacer(1, 10))
    
    table_data = [
        [
            Paragraph("<b>Date</b>", styles['Normal']),
            Paragraph("<b>Party Name</b>", styles['Normal']),
            Paragraph("<b>Type</b>", styles['Normal']),
            Paragraph("<b>Quantity</b>", styles['Normal']),
            Paragraph("<b>Amount (Rs)</b>", styles['Normal'])
        ]
    ]
    
    transactions = Transaction.query.order_by(Transaction.id.desc()).all()
    for t in transactions:
        t_type = "Income" if t.type == 'Income' else "Expense"
        table_data.append([
            Paragraph(str(t.date), styles['Normal']),
            Paragraph(str(t.party_name), styles['Normal']),
            Paragraph(t_type, styles['Normal']),
            Paragraph(str(t.quantity), styles['Normal']),
            Paragraph(f"Rs. {t.amount}", styles['Normal'])
        ])
    
    col_widths = [90, 140, 90, 105, 105]
    pdf_table = Table(table_data, colWidths=col_widths)
    
    pdf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')]),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
    ]))
    
    elements.append(pdf_table)
    doc.build(elements)
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="peanut_master_report.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)