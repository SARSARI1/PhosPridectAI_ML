import os
from flask import Flask, redirect, url_for, render_template, request, session, make_response
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
import pickle
from matplotlib.offsetbox import DrawingArea
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import scipy.stats as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.platypus import Image,Spacer
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#-----------------------------------------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key="hello"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///feedbacks.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#------------------------------------------------------------load models--------------------------------------------------------------

# Load the model quantity of phosphate 
loaded_model_q = pickle.load(open('modelQuantity_RFR.pkl', 'rb'))

# Load the model price  of phosphate
loaded_model_p= pickle.load(open('model_price_RFR.pkl','rb'))

# ---------------------------------------------------------------------Create some  dictionarys-------------------------------------- :

month_dict = {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}

countries ={'Afghanistan': 0, 'Albania': 1, 'Algeria': 2, 'Angola': 3, 'Argentina': 4, 'Armenia': 5, 'Australia': 6, 'Azerbaijan': 7, 'Bahamas': 8, 'Bahrain': 9, 'Bangladesh': 10, 'Belarus': 11, 'Belgium': 12, 'Belize': 13, 'Benin': 14, 'Bhutan': 15, 'Bolivia': 16, 'Bosnia and Herzegovina': 17, 'Botswana': 18, 'Brazil': 19, 'Brunei': 20, 'Bulgaria': 21, 'Burkina Faso': 22, 'Burundi': 23, 'Cambodia': 24, 'Cameroon': 25, 'Canada': 26, 'Central African Republic': 27, 'Chile': 28, 'China': 29, 'Colombia': 30, 'Congo': 31, 'Costa Rica': 32, 'Croatia': 33, 'Cuba': 34, 'Cyprus': 35, 'Czechia': 36, 'Democratic Republic of Congo': 37, 'Denmark': 38, 'Dominican Republic': 39, 'Ecuador': 40, 'Egypt': 41, 'El Salvador': 42, 'Eritrea': 43, 'Estonia': 44, 'Ethiopia': 45, 'Fiji': 46, 'Finland': 47, 'France': 48, 'Gabon': 49, 'Gambia': 50, 'Georgia': 51, 'Germany': 52, 'Ghana': 53, 'Greece': 54, 'Guatemala': 55, 'Guinea': 56, 'Guyana': 57, 'Honduras': 58, 'Hungary': 59, 'Iceland': 60, 'India': 61, 'Indonesia': 62, 'Iran': 63, 'Iraq': 64, 'Ireland': 65, 'Israel': 66, 'Italy': 67, 'Jamaica': 68, 'Japan': 69, 'Jordan': 70, 'Kazakhstan': 71, 'Kenya': 72, 'Kuwait': 73, 'Kyrgyzstan': 74, 'Latvia': 75, 'Lebanon': 76, 'Libya': 77, 'Lithuania': 78, 'Luxembourg': 79, 'Madagascar': 80, 'Malawi': 81, 'Malaysia': 82, 'Mali': 83, 'Malta': 84, 'Mauritius': 85, 'Mexico': 86, 'Moldova': 87, 'Mongolia': 88, 'Montenegro': 89, 'Morocco': 90, 'Mozambique': 91, 'Myanmar': 92, 'Namibia': 93, 'Nepal': 94, 'Netherlands': 95, 'New Caledonia': 96, 'New Zealand': 97, 'Nicaragua': 98, 'Niger': 99, 'Nigeria': 100, 'North Korea': 101, 'North Macedonia': 102, 'Norway': 103, 'Oman': 104, 'Pakistan': 105, 'Panama': 106, 'Papua New Guinea': 107, 'Paraguay': 108, 'Peru': 109, 'Philippines': 110, 'Poland': 111, 'Portugal': 112, 'Qatar': 113, 'Romania': 114, 'Russia': 115, 'Rwanda': 116, 'Saudi Arabia': 117, 'Senegal': 118, 'Serbia': 119, 'Serbia and Montenegro': 120, 'Slovakia': 121, 'Slovenia': 122, 'South Africa': 123, 'South Korea': 124, 'Spain': 125, 'Sri Lanka': 126, 'Sudan': 127, 'Suriname': 128, 'Sweden': 129, 'Switzerland': 130, 'Syria': 131, 'Taiwan': 132, 'Tajikistan': 133, 'Tanzania': 134, 'Thailand': 135, 'Togo': 136, 'Trinidad and Tobago': 137, 'Tunisia': 138, 'Turkey': 139, 'Turkmenistan': 140, 'Uganda': 141, 'Ukraine': 142, 'United Arab Emirates': 143, 'United Kingdom': 144, 'United States': 145, 'Uruguay': 146, 'Uzbekistan': 147, 'Venezuela': 148, 'Vietnam': 149, 'World': 150, 'Yemen': 151, 'Zambia': 152, 'Zimbabwe': 153}



#------------------------------------------------------------------------------------Sessions-------------------------------------------------------: 

app.permanent_session_lifetime=timedelta(minutes=5)

#---------------------------------------------------------------------------------------database--------------------------------------------------------------

db=SQLAlchemy(app)

class feedback(db.Model):
    __id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    message = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)  

    def __init__(self, name, message):
        self.name = name
        self.message = message
        self.date = datetime.now() 
  
#----------------------------------------------------------------------------------------------------functions----------------------------------------------------------------:

# generate pdf function :
def generate_pdf(session_values, country_name, year, nutrient_potash, nutrient_nitrogen,diesel,diesel_roc,phosphate_diesel_ratio,phosphate_quantity):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    # Add logo
    logo_path = r'static\images\1-removebg-preview.png'
    logo = Image(logo_path, width=300, height=300)
    elements.append(logo)
    # Add space below the logo
    elements.append(Spacer(1, 20))
    # Add title
    title = f"Annual Report of {country_name} - Year {year}"
    elements.append(Paragraph(title, getSampleStyleSheet()['Title']))
    elements.append(PageBreak())  # Move to the next page
    # Add nutrient quantities
    # Center the following elements and add more spacing
    style_center = getSampleStyleSheet()['BodyText']
    style_center.alignment = 1  # Center alignment
    date = f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
   # Add the date with centered style
    style_center = getSampleStyleSheet()['Normal']
    style_center.alignment = 1  # 1 indicates centered alignment

    # Create a new Paragraph with "Date:" in bold
    date_text = "<b>Date:</b> " + date
    date_paragraph = Paragraph(date_text, style_center)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 2))
    elements.append(Paragraph(f"<b>Nutrient Potash (tonnes):</b> {float(nutrient_potash):.2f}", style_center))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph(f"<b>Nutrient Nitrogen  (tonnes):</b> {float(nutrient_nitrogen):.2f}", style_center))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph(f"<b>phosphate quantity (tonnes):</b> {float(phosphate_quantity):.2f}", style_center))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph(f"<b>Diesel ROC:</b> {diesel_roc}", style_center))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph(f"<b>Diesel price(dollars):</b> {diesel}", style_center))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph(f"<b>Phosphate/Diesel Price Ratio:</b> {phosphate_diesel_ratio}", style_center))
    elements.append(Spacer(1, 20))  # Additional spacing below the elements

    # Create data for the chart
    chart_data = [(month, values['predicted_price']) for month, values in session_values.items()]

        # Create a smaller drawing for the chart
    chart_width = 400
    chart_height = 200
    drawing = Drawing(chart_width, chart_height)
    
    
    # Create a LinePlot with a smaller size
    lp = LinePlot()
    lp.x = 40  # Center the plot horizontally
    lp.y = 0  # Center the plot vertically
    lp.height = chart_height - 50  # Adjust height
    lp.width = chart_width - 100   # Adjust width
    lp.data = [chart_data]
    lp.joinedLines = 1
    lp.lines[0].symbol = makeMarker('FilledCircle')
    lp.lines[0].strokeColor = colors.blue
    lp.lines[0].strokeWidth = 2

    drawing.add(lp)

    # Add a label to the chart
    chart_label = Paragraph("Predicted Prices Over Months", getSampleStyleSheet()['BodyText'])
  
    elements.append(drawing)
    elements.append(Spacer(1, 10))
    elements.append(chart_label)
    elements.append(Spacer(1, 40))
    

    # Create data for the table
    table_data = [['Month', 'Predicted Price']]
    
    # Define month names as strings
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    for month, values in session_values.items():
        predicted_price = f"{values['predicted_price']:.6f}$"
        month_str = month_names[month - 1]  # Convert month to string
        table_data.append([month_str, predicted_price])

    

    
    # Create the table and add it to the elements
    table = Table(table_data, colWidths=[150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer




#predict quntity of phosphate function : 

def predict_quantity(country,yr,n_p,n_n):
    scaler = StandardScaler()
    country = int(country)+1
    yr = int(yr)
    n_p = float(n_p)
    n_n = float(n_n)

    input_test = pd.DataFrame({'Entity': [country],
        'Year': [yr],
            'Nutrient potash':[n_p],
            'Nutrient nitrogen': [n_n]
        })

    pred_mlr_july = loaded_model_q.predict(input_test)
    result=pred_mlr_july[0]
    return result


#predict price of phosphate function :
def predict_price(year_one,mth,diesel_roc,diesel_p,phosphate_d_r):
    year_one = int(year_one)  
    mth = int(mth)
    diesel_roc = float(diesel_roc)
    diesel_p = float(diesel_p)
    phosphate_d_r  = float(phosphate_d_r)
    #predictooin model use
    input_test = pd.DataFrame({ 'Month':[mth],
    'Year': [year_one],
    'Diesel Price (Dollars US par gallon)': [diesel_p],
    'Diesel ROC':[diesel_roc],
    'Phosphate/Diesel Price Ratio': [phosphate_d_r]
     })
    #getting the prediction value 
    pred_RFR_july = loaded_model_p.predict(input_test)
    result= pred_RFR_july[0]
    return result





# -------------------------------------------------------Routes----------------------------------------------------------------------------------------- :

@app.route("/")
def home():
    Feedbacks = feedback.query.all()
    return render_template('home.html', feedbacks=Feedbacks)

@app.route("/home")
def logo():
    Feedbacks = feedback.query.all()
    return render_template('home.html', feedbacks=Feedbacks)

@app.route("/index")
def index():
    return render_template('prediction.html') 

@app.route("/price")
def price():
    return render_template('result_price.html')

@app.route("/quantity")
def quantity():
    return render_template('result_quantity.html')

@app.route("/turnover")
def turnover():
    return render_template('result_turnover.html')

@app.route("/pricePredicted")
def pricePredicted():
    return render_template('predictedPrice.html')

@app.route("/quantityPredicted")
def quantityPredicted():
    return render_template('predictedQuantity.html')



@app.route("/submit_feedback",methods=["POST","GET"])
def submit_feedback():
    if request.method=="POST":
        session.permanent=True
        nm=request.form["name"]
        msg=request.form["message"]
        #store the feedback on the database
        feedbk = feedback(name=nm,message=msg)
        db.session.add(feedbk)
        db.session.commit()

    #display all of the feedbacks stored in database
    Feedbacks = feedback.query.all()
    return render_template('home.html', feedbacks=Feedbacks)




#Make prediction to quntity of phosphate
@app.route("/make_predictions_quantity", methods=["POST"])
def make_predictions_quantity():
    if request.method=="POST":
        session.permanent=True
        #get the user input
        country=request.form["country"]
        yr=request.form["year"]
        n_p=request.form["Nutrient_potash"]
        n_n=request.form["Nutrient_nitrogen"]
        #storing the values of entity and year on a session 
        session["Entity"]=list(countries.keys())[list(countries.values()).index(int(country))]
        session["Year"]=yr
        session["phosphate_quantity"]=predict_quantity(country,yr,n_p,n_n)

    return render_template('predictedQuantity.html')  


#Make prediction to price of phosphate
@app.route("/make_predictions_price", methods=["POST"])
def make_predictions_price():
    if request.method=="POST":
        session.permanent=True
        year_one=request.form["year1"]
        mth=request.form["month"]
        diesel_p=request.form["Diesel"]
        diesel_roc=request.form["Diesel_ROC"]
        phosphate_d_r=request.form["Phosphate_Diesel_Price_Ratio"]
        #storing the resutls on a session
        session["year1"]=year_one
        session["month"]=list(month_dict.values())[list(month_dict.keys()).index(str(mth))]
        session["phosphate_price"]=predict_price(year_one,mth,diesel_roc,diesel_p,phosphate_d_r)

    return render_template('predictedPrice.html')


#make priction to both price and quantity
@app.route("/make_predictions_turnover", methods=["POST"])
def make_predictions_turnover():
    if request.method=="POST":
        #start session
        session.permanent=True
        #get user input:
        country_turnover=request.form["country"]
        yr_turnover=request.form["year"]
        n_p_turnover=request.form["Nutrient_potash"]
        n_n_turnover=request.form["Nutrient_nitrogen"]
        mth_turnover=request.form["month"]
        diesel_p_turnover=request.form["Diesel"]
        diesel_roc_turnover=request.form["Diesel_ROC"]
        phosphate_d_r_turnover=request.form["Phosphate_Diesel_Price_Ratio"]
        #storing the values on session 
        session["Entity_turnover"]=list(countries.keys())[list(countries.values()).index(int(country_turnover))]
        session["Nutrient_potash"]=n_p_turnover
        session["Nutrient_nitrogen"]=n_n_turnover
        session["month_turnover"]=list(month_dict.values())[list(month_dict.keys()).index(str(mth_turnover))]
        session["phosphate_price_turnover"]=predict_price(yr_turnover,mth_turnover,diesel_roc_turnover,diesel_p_turnover,phosphate_d_r_turnover)
        session["Year_turnover"]=yr_turnover
        session["phosphate_quantity_turnover"]=predict_quantity(country_turnover,yr_turnover,n_p_turnover,n_n_turnover)
        session["Diesel_ROC"]=diesel_roc_turnover
        session["Diesel"]=diesel_p_turnover
        session["Phosphate_Diesel_Price_Ratio"]=phosphate_d_r_turnover
        # Iterate through all months and predict phosphate prices
        for month in range(1, 13):
            # Store the predicted price for the current month in the session
            session[f"predicted_phosphate_price_month_{month}"] =predict_price(yr_turnover,month,diesel_roc_turnover,diesel_p_turnover,phosphate_d_r_turnover)

    return render_template('predictedTurnover.html')



#download the report that contains all results (price of each month and the input of user also the quntity prediction)
@app.route("/download_pdf", methods=["GET"])
def download_pdf():
    predicted_prices = {}
    country_name = session.get("Entity_turnover", "")
    year = session.get("Year_turnover", "")
    nutrient_potash = session.get("Nutrient_potash", "")
    nutrient_nitrogen = session.get("Nutrient_nitrogen", "")
    phosphate_quantity_turnover=session.get("phosphate_quantity_turnover", "")

    for month in range(1, 13):
        predicted_price = session.get(f"predicted_phosphate_price_month_{month}", "")
        diesel_price = session.get("Diesel", "")
        diesel_roc = session.get("Diesel_ROC", "")
        phosphate_diesel_ratio = session.get("Phosphate_Diesel_Price_Ratio", "")
        
        predicted_prices[month] = {
            "predicted_price": predicted_price,
            "diesel_price": diesel_price,
            "diesel_roc": diesel_roc,
            "phosphate_diesel_ratio": phosphate_diesel_ratio,
        }

    pdf_buffer = generate_pdf(predicted_prices, country_name, year, nutrient_potash, nutrient_nitrogen,diesel_price,diesel_roc,phosphate_diesel_ratio,phosphate_quantity_turnover)

    response = make_response(pdf_buffer.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=report_{country_name}_{year}.pdf"

    return response

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,host='0.0.0.0')

   