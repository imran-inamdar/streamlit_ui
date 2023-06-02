# Core Pkgs
import streamlit as st 
import streamlit.components.v1 as stc
 

# Data Pkgs
import pandas as pd 
from faker import Faker
import xml.etree.ElementTree as ET
import numpy as np

# Utils
import base64
import time 
timestr = time.strftime("%Y%m%d-%H%M%S")


# Fxn to Download
def make_downloadable_df(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()  # B64 encoding
    st.markdown("Download CSV File")
    new_filename = "fake_dataset_{}.csv".format(timestr)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)

# Fxn to Download Into A Format
def make_downloadable_df_format(data,format_type="csv"):
	if format_type == "csv":
		datafile = data.to_csv(index=False)
	elif format_type == "json":
		datafile = data.to_json()
	b64 = base64.b64encode(datafile.encode()).decode()  # B64 encoding
	st.markdown("Download File")
	new_filename = "fake_dataset_{}.{}".format(timestr,format_type)
	href = f'<a href="data:file/{format_type};base64,{b64}" download="{new_filename}">Click Here!</a>'
	st.markdown(href, unsafe_allow_html=True)


# Generate A Simple Profile
def generate_profile(number,random_seed=1):
	fake = Faker()
	Faker.seed(random_seed)
	data = [fake.simple_profile() for i in range(number)]
	df = pd.DataFrame(data)
	return df 

# Generate A Customized Profile Per Locality
def generate_locale_profile(number,locale,random_seed=1):
	locale_fake = Faker(locale)
	Faker.seed(random_seed)
	data = [locale_fake.simple_profile() for i in range(number)]
	df = pd.DataFrame(data)
	return df


def generate_credit_profile(number, random_seed=1):
	fake = Faker("en_US")
	account_holder_name = []
	account_number=[]
	account_type=[]
	bank_name=[]
	contact=[]
	creditpro = []
	cardnum = []
	cred_sec_code = []
	cred_expire = []
	zipcode = []
	account_balance=[]
	Faker.seed(random_seed)
	for _ in range(number):
		account_holder_name.append(fake.name())
		account_number.append(fake.random_int(min=1000000000, max=9999999999, step=1))
		account_balance.append(np.random.randint(100,50000))
		account_type.append(fake.random_element(elements=("checking", "savings", "money market")))
		bank_name.append(fake.random_element(elements=("Chase", "Wells Fargo", "Bank of America", "Citibank")))
		contact.append(fake.phone_number())
		cre=creditpro.append(fake.credit_card_provider())
		cardnum.append(fake.credit_card_number(cre))
		cred_sec_code.append(fake.credit_card_security_code())
		cred_expire.append(fake.credit_card_expire())
		zipcode.append(fake.zipcode())

	df = pd.DataFrame(zip(account_holder_name,account_number,account_balance,account_type,bank_name,contact,creditpro, cardnum,cred_sec_code, cred_expire, zipcode),
					  columns=['Account_holder_name','Account_number','Account_balance','Account_type','Bank_name','Contact Number','credit card provider', 'Credit card number','Security Code', 'Expiry Date', 'zipcode'])
	return df



def main():
	st.title("Fake Data Generator")
	#stc.html(custom_title)

	menu = ["Simple","Customize","Banking Data"]

	choice = st.sidebar.selectbox("Menu",menu)
	if choice == "Simple":
		st.subheader("Simple")
		number_to_gen = st.sidebar.number_input("Number",10,100000)
		localized_providers = ["ar_AA", "ar_EG", "ar_JO", "ar_PS", "ar_SA", "bg_BG", "bs_BA", "cs_CZ", "de", "de_AT", "de_CH", "de_DE", "dk_DK", "el_CY", "el_GR", "en", "en_AU", "en_CA", "en_GB", "en_IE", "en_IN", "en_NZ", "en_PH", "en_TH", "en_US", "es", "es_CA", "es_ES", "es_MX", "et_EE", "fa_IR", "fi_FI", "fil_PH", "fr_CA", "fr_CH", "fr_FR", "fr_QC", "he_IL", "hi_IN", "hr_HR", "hu_HU", "hy_AM", "id_ID", "it_CH", "it_IT", "ja_JP", "ka_GE", "ko_KR", "la", "lb_LU", "lt_LT", "lv_LV", "mt_MT", "ne_NP", "nl_BE", "nl_NL", "no_NO", "or_IN", "pl_PL", "pt_BR", "pt_PT", "ro_RO", "ru_RU", "sk_SK", "sl_SI", "sv_SE", "ta_IN", "th", "th_TH", "tl_PH", "tr_TR", "tw_GH", "uk_UA", "zh_CN", "zh_TW"]
		locale = st.sidebar.multiselect("Select Locale",localized_providers,default="en_US")
		dataformat = st.sidebar.selectbox("Save Data As",["csv","json"])

		df = generate_locale_profile(number_to_gen,locale)
		st.dataframe(df)

		#to rename column names
		col_to_change=st.multiselect("To Change Column name Select Column names from list:",df.columns)
		st.write("You Selected:",col_to_change)

		new_column_name=[]
		for item in col_to_change:
			new_column_name.append(st.text_input(item,value=item))
		dict = {}
		for key in col_to_change:
			for value in new_column_name:
				dict[key] = value
				new_column_name.remove(value)
				break

		df.rename(columns=dict,
				  inplace=True)

		#col_dt_change=st.multiselect("To Change Column datatype, Select Column names from list:",df.columns)
		
		st.dataframe(df)
		

		with st.expander("Download"):
			make_downloadable_df_format(df,dataformat)
		return
	elif choice == "Customize":
		st.subheader("Customize Your Fields")
		# Locale Providers For Faker Class
		localized_providers = ["ar_AA", "ar_EG", "ar_JO", "ar_PS", "ar_SA", "bg_BG", "bs_BA", "cs_CZ", "de", "de_AT", "de_CH", "de_DE", "dk_DK", "el_CY", "el_GR", "en", "en_AU", "en_CA", "en_GB", "en_IE", "en_IN", "en_NZ", "en_PH", "en_TH", "en_US", "es", "es_CA", "es_ES", "es_MX", "et_EE", "fa_IR", "fi_FI", "fil_PH", "fr_CA", "fr_CH", "fr_FR", "fr_QC", "he_IL", "hi_IN", "hr_HR", "hu_HU", "hy_AM", "id_ID", "it_CH", "it_IT", "ja_JP", "ka_GE", "ko_KR", "la", "lb_LU", "lt_LT", "lv_LV", "mt_MT", "ne_NP", "nl_BE", "nl_NL", "no_NO", "or_IN", "pl_PL", "pt_BR", "pt_PT", "ro_RO", "ru_RU", "sk_SK", "sl_SI", "sv_SE", "ta_IN", "th", "th_TH", "tl_PH", "tr_TR", "tw_GH", "uk_UA", "zh_CN", "zh_TW"]
		locale = st.sidebar.multiselect("Select Locale",localized_providers,default="en_US")
		
		profile_options_list = ['username','name','sex' ,'address','mail' ,'birthdate','job','company','ssn','residence','current_location','blood_group', 'website']
		profile_fields = st.sidebar.multiselect("Select Fields",profile_options_list,default='username')
		#number_to_gen = st.sidebar.number_input("Number", 10, 100000)
		number_to_gen = st.sidebar.slider("Select Number of Records", 10, 10000)
		dataformat = st.sidebar.selectbox("Save Data As", ["csv", "json"])
		# Initialize Faker Class
		custom_fake = Faker(locale)
		data = [custom_fake.profile(fields=profile_fields) for i in range(number_to_gen)]
		df = pd.DataFrame(data)


		# Initialize Faker Class
		custom_fake = Faker(locale)
		data = [custom_fake.profile(fields=profile_fields) for i in range(number_to_gen)]
		df = pd.DataFrame(data)
		st.dataframe(df)
		# to rename column names
		col_to_change = st.multiselect("To Change Column name Select Column names from list:", df.columns)
		st.write("You Selected:", col_to_change)

		new_column_name = []
		for item in col_to_change:
			new_column_name.append(st.text_input(item, value=item))
		dict = {}
		for key in col_to_change:
			for value in new_column_name:
				dict[key] = value
				new_column_name.remove(value)
				break

		df.rename(columns=dict,
				  inplace=True)
		# View As Dataframe
		st.dataframe(df)

		# View as JSON
		with st.expander("🔍: View JSON "):
			st.json(data)

		with st.expander("Download"):
			make_downloadable_df_format(df,dataformat)
	elif choice=="Banking Data":
		#st.subheader("Banking Data ")
		st.subheader("Banking  Data")
		# Locale Providers For Faker Class



		#number_to_gen = st.sidebar.number_input("Number", 10, 100000)
		number_to_gen = st.sidebar.slider("Select Number of Records", 10, 100000)
		df = generate_credit_profile(number_to_gen)
		dataformat = st.sidebar.selectbox("Save Data As", ["csv", "json"])
		


		# number_to_gen = st.sidebar.number_input("Number",10,50000)
		# dataformat = st.sidebar.selectbox("Save Data As",["csv","json"])

		# Initialize Faker Class
		#custom_fake = Faker(locale)
		#data = [custom_fake.profile(fields=profile_fields) for i in range(number_to_gen)]
		#df = pd.DataFrame(data)

		# View As Dataframe
		st.dataframe(df)
		# to rename column names
		col_to_change = st.multiselect("To Change Column name Select Column names from list:", df.columns)
		st.write("You Selected:", col_to_change)

		new_column_name = []
		for item in col_to_change:
			new_column_name.append(st.text_input(item, value=item))
		dict = {}
		for key in col_to_change:
			for value in new_column_name:
				dict[key] = value
				new_column_name.remove(value)
				break

		df.rename(columns=dict,
				  inplace=True)

		# col_dt_change=st.multiselect("To Change Column datatype, Select Column names from list:",df.columns)

		st.dataframe(df)
		# View as JSON
		#with st.expander("🔍: View JSON "):
			#st.json(df)

		with st.expander("Download"):
			make_downloadable_df_format(df, dataformat)

	else:
		st.subheader("About")
		







if __name__ == '__main__':
	main()
