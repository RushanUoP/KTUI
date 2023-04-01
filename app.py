import streamlit as st
import mysql.connector
import pandas as pd
from PIL import Image
#from session_state import SessionState
is_logged_in = False
# Connect to MySQL database
def create_connection():
    conn = mysql.connector.connect(
        host="eu-cdbr-west-03.cleardb.net",
        user="b76a0cd64214a2",
        password="9e1e2d91",
        database="heroku_53bd8d966df0668"
    )
    return conn

conn = create_connection()
conn = create_connection()
headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()
 

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="KTLogo.png", width=150, height=160)




def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    
def show_logout_page():
    loginSection.empty();
    with logOutSection:
        st.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)
    
def LoggedIn_Clicked(userName, password):
    if login(userName, password):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False;
        st.error("Invalid user name or password")
    
def show_login_page():
    
    with loginSection:
        st.image(my_logo)
        st.title("Welcome to KT Database Application! \n Enter Your Credentials to Login!")
        st.session_state['loggedIn'] = False
        if st.session_state['loggedIn'] == False:
            userName = st.text_input (label="Username", value="", placeholder="Enter your user name")
            password = st.text_input (label="Password", value="",placeholder="Enter password", type="password")
            st.button ("Login", on_click=LoggedIn_Clicked, args= (userName, password))


def main():
    
    
    #first run will have nothing in session_state
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page() 
    else:
        if st.session_state['loggedIn']:
            show_logout_page()    
            data()  
        else:
            show_login_page()




def login(username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False







        


def data():
   
    
    with mainSection:
        st.image(my_logo)
        
            
        st.write("# Welcome to KT Database Exploration")
        #session_state = SessionState.get(username="")

        #if not session_state.username:
            #st.error("Please log in to continue.")
            #return

        #st.write(f"Welcome {session_state.username}!")
        # Sidebar menu
        st.sidebar.title("Menu")
        menu = st.sidebar.radio("Select an option", ("Insert Data", "View Data"))

        # Insert Data
        if menu == "Insert Data":
            st.title("Insert Data")
            table = st.radio("Select Type of Data to Enter", ("Organisation","Species", "Project Type","Vessel" ,"Project Vessel" ,"Vessel Regulatory Body" ,"Project","Project Team", "Certification Type", "Certification", "Stakeholder","Consultant"))
            
            if table == "Organisation":
                org_id = st.text_input("Organization ID")
                org_type = st.text_input("Organization Type")
                org_name = st.text_input("Organization Name")
                address = st.text_input("Address")
                post_code= st.text_input("Post Code")
                country = st.text_input("Country")
                contact_person = st.text_input("Contact Person")
                org_email = st.text_input("Email")
                number = st.text_input("Contact")
                vessel_count = st.text_input("Vessel Count")
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO organisation (OrgId,OrgType,OrgName,Address,PostCode,Country,ContactPerson,Email,ContactNo,VesselCount) VALUES (%s,%s,%s,%s,%s,(select CountryId FROM country WHERE CountryName =%s),%s,%s,%s,%s)", (org_id,org_type,org_name,address,post_code,country,contact_person,org_email,number,vessel_count,))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()
            
            elif table == "Species":
                common_name = st.text_input("Common Name")
                scientific_name = st.text_input("Scientific Name")
                #c_name = st.text_input("Certification Name")
                #c_no = int(st.text_input("Certification Number"))
                
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO species (CommanName,ScientificName) VALUES (%s,%s)", (common_name,scientific_name,))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()
        

            elif table == "Vessel":
                uvi_no = st.text_input("UVI No.")
                uvi_type = st.text_input("UVI Type")
                orga_id = st.text_input("Organisation ID")
                vessel_name = st.text_input("Vessel Name")
                owner_name = st.text_input("Owner Name")
                owner_country = st.text_input("Owner Country")
                op_name= st.text_input("Operator Name")
                flag_state = st.text_input("Flag State")
                gear_type = st.text_input("Gear Type")
                vessel_length = st.text_input("Vessel Length")
                hold_capacity = st.text_input("Hold Capacity")
                em = st.text_input("Electronic Monitoring (0 or 1)")
                em_date = st.text_input("Electronic Monitoring Fitting Date (YYYY-MM-DD)")
                irc_sign = st.text_input("IRC Sign")
                #nat_reg_no = st.text_input("National Reg No.")
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO vessel (UVIno,UVIType,OrgId,VesselName,OwnerName,OwnerCountry,OperatorName,FlagState, GearType,VesselLength,HoldCapacity,EM,EMFittingDate,IRCSign) VALUES (%s,%s,(SELECT OrgId from organisation WHERE OrgId = %s),%s,%s,(SELECT CountryId from country WHERE CountryName = %s),%s,%s,%s,%s,%s,%s,%s,%s)", (uvi_no, uvi_type,orga_id,vessel_name,owner_name,owner_country,op_name,flag_state,gear_type,vessel_length,hold_capacity,em,em_date,irc_sign))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()       
            elif table == "Project Vessel":
                uvi_no_pv = st.text_input("UVI No.")
                p_code_pv = st.text_input("Project Code")
                fishing_area = st.text_input("Fishing Area")
                landing_port = st.text_input("Landing Port")
                last_port_date = st.text_input("Last Port Date (YYYY-MM-DD)")
                last_trip_date = st.text_input("Last Trip Obs Date")
                crew_count= st.text_input("Crew Count")
                crew_nationality = st.text_input("Crew Nationality")
                crew_list = st.text_input("Crew List")
                audit_date = st.text_input("Audit Date (YYYY-MM-DD)")
                audit_ref = st.text_input("Audit Reference")
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO projectvessel (UVINo, ProjectCode, FishingArea,LandingPort,LastPortDate,LastTripObsvDate,CrewCount,CrewNationality,CrewList,AuditDate,AuditRef) VALUES ((SELECT UVINo from vessel where UVINo =%s),(SELECT ProjectCode from project WHERE ProjectCode =%s),%s,%s,%s,%s,%s,%s,%s,%s,%s)", (uvi_no_pv, p_code_pv, fishing_area,landing_port,last_port_date,last_trip_date,crew_count,crew_nationality,crew_list,audit_date,audit_ref,))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()       
            elif table == "Vessel Regulatory Body":
                uvi_no_vrb = st.text_input("UVI No.")
                rfmo_type = st.text_input("RFMO Type")
                reg_no = st.text_input("Registration No.")
                start_date = st.text_input("Start Date (YYYY-MM-DD)")
                end_date = st.text_input("End Date (YYYY-MM-DD)")
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO vesselregulatorybody (UVINo, RFMOType,RegNo,StartDate,EndDate) VALUES ((SELECT UVINo FROM vessel WHERE UVINo = %s),%s,%s,%s,%s)", (uvi_no_vrb,rfmo_type,reg_no,start_date,end_date,))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()      

            elif table == "Certification":
                company = st.text_input("Company")
                vessel = st.text_input("Vessel")
                c_name = st.text_input("Certification Name")
                c_no = st.text_input("Certification Number")
                
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO certification (Company, Vessel, CertificationName,CertificationNo) VALUES ((select OrgId from organisation where OrgName= %s),(select UVINo from vessel where VesselName= %s),(select CertificationName from certificationtype where CertificationName= %s),%s)", (company, vessel, c_name,c_no,))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()
                    
            elif table == "Certification Type":
                c_name = st.text_input("Certification Name")
                c_desc = st.text_input("Certification Description")
                
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO certificationtype (CertificateDescription) VALUES (%, %s)", (c_name,c_desc,))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()
                    
            elif table == "Consultant":
                c_id = st.text_input("ConsultantID")
                c_type = st.text_input("Consultant Type")
                c_pswd = st.text_input("Password")
                c_fname = st.text_input("First Name")
                c_lname = st.text_input("Last Name")
                c_designation = st.text_input("Designation")
                c_review = st.text_input("ConsultantReview")

                
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO consultant (ConsultantID, ConsultantType, Pswd,ConsultantFirstName,ConsultantLastName,ConsultantDesignation, ConsultantReviews) VALUES (%s, %s, %s,%s,%s,%s,%s)", (c_id, c_type,c_pswd, c_fname,c_lname,c_designation, c_review))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()
            elif table == "Project Type":
                proj_type = st.text_input("Projet Type")
                proj_desc = st.text_input("Description")

                
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO projecttype (ProjectType, ProjectTypeDesc) VALUES (%s, %s)", (proj_type,proj_desc,))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()
            elif table == "Project":
                p_code = st.text_input("Project Code")
                client_type = st.text_input("Client Type")
                client_id_p = st.text_input("Organisation ID")
                p_name = st.text_input("Project Name")
                p_desc = st.text_input("Project description")
                tors = st.text_input("Terms of Reference")
                p_start_date = st.text_input("Start Date (YYYY-MM-DD)")
                p_end_date = st.text_input("End Date (YYYY-MM-DD)")

                
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO project (ProjectCode,  ClientType, ClientId, ProjectName, ProjectDescription, TermsOfReference, StartDate, EndDate) VALUES (%s, %s,(SELECT OrgId from organisation WHERE OrgId =%s), %s,%s,%s,%s, %s)", (p_code, client_type, client_id_p, p_name, p_desc, tors, p_start_date, p_end_date))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()
            elif table == "Project Team":
                pro_code = st.text_input("Project")
                consulttant_id = st.text_input("Consultant ID")
                p_role = st.text_input("Project Role")
                no_days = st.text_input("Number of Days")
            

                
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO projectteam (ProjectCode, ConsultantId ,ProjectRole,  No_of_Days) VALUES (select ProjectCode from project where ProjectName= %s), (select ConsultantId from consultant where ConsultantId= %s),%s, %s)", (pro_code, consulttant_id, p_role, no_days))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()
            elif table == "Stakeholder":
                p_code_stk = st.text_input("Project Code")
                stakeholder_id = st.text_input("Stakeholder ID")
                p_role = st.text_input("Project Role")
                no_days = st.text_input("Number of Days")
            

                
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO projectteam (ProjectCode, StakeholderId) VALUES (select ProjectCode from project where ProjectCode= %s), (select OrgId from organisation where OrgId= %s),%s, %s)", (pro_code_stk, stakeholder_id,))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()

            elif table == "Country":
                country_id = st.text_input("Country ID")
                country_name = st.text_input("Country Name")
            

                
                if st.button("Submit"):
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO country (CountryId,  CountryName) VALUES (%s, %s)", (country_id, country_name))
                    conn.commit()
                    st.success("Data inserted successfully!")
                    cursor.close()

        # View Data
        elif menu == "View Data":
            st.title("View Data")
            table = st.radio("Select Type of Data to View", ("Organisation","Vessel","Species","Organisation Species","Project Vessel","Vessel Regulatory Body","Project","Project Team" ,"Certification", "Certification Type", "Consultant", "Stakeholder","Country"))
            
            if table == "Organisation":
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM organisation")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["OrgId","OrgType","OrgName","Address","PostCode","Country","ContactPerson","Email","ContactNo","VesselCount"]) 
                st.dataframe(df)
                cursor.close()
            if table == "Vessel":
                cursor = conn.cursor()
                cursor.execute('SELECT UVINo, UVIType, v.OrgId, VesselName, OwnerName, v.OwnerCountry, OperatorName, FlagState, GearType, VesselLength, HoldCapacity, EM, EMFittingDate, IRCSign FROM vessel v INNER JOIN organisation o ON v.OrgId = o.OrgId INNER JOIN country c ON v.OwnerCountry =c.CountryId')		
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["UVINo", "UVIType", "OrgId", "VesselName", "OwnerName", "OwnerCountry", "OperatorName", "FlagState", "GearType", "VesselLength", "HoldCapacity", "EM", "EMFittingDate", "IRCSign"]) 
                st.dataframe(df)
                cursor.close()
            if table == "Organisation Species":
                cursor = conn.cursor()
                cursor.execute("""SELECT `orgspecies`.`OrgId` as "Organisation Id",
OrgName as "Organisation Name",
    `orgspecies`.`TargetSpecies` as "Target Species",
    `orgspecies`.`BaitSpecies` as "Bait Species"
FROM `heroku_53bd8d966df0668`.`orgspecies`
INNER join organisation on organisation.OrgId=orgspecies.orgId""")		
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["Organisation ID", "Organisation Name", "Target Species", "Bait Species"]) 
                st.dataframe(df)
                cursor.close()
            
            
            if table == "Species":
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM species")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["CommonName","ScientificName"]) 
                st.dataframe(df)
                cursor.close()
              
            if table == "Project Vessel":
                cursor = conn.cursor()
                cursor.execute("""
SELECT `projectvessel`.`UVINo` as "UVI No.",
    VesselName as "Vessel Name",
    `projectvessel`.`ProjectCode` as "Project Code",
    `projectvessel`.`FishingArea` as "Fishing Area",
    `projectvessel`.`LandingPort` as "Landing Port",
    `projectvessel`.`LastPortDate` as "LastPortDate",
    `projectvessel`.`LastTripObsvDate` as "LastTripObsvDate",
    `projectvessel`.`CrewCount` as "Crew Count",
    `projectvessel`.`CrewNationality` as "Crew Nationality",
    `projectvessel`.`CrewList` as "Crew List",
    `projectvessel`.`AuditDate` as "Audit Date",
    `projectvessel`.`AuditRef` as "Audit Ref."
FROM `heroku_53bd8d966df0668`.`projectvessel`
INNER JOIN `vessel` ON `vessel`.`UVINo` = `projectvessel`.`UVINo`
""")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["UVINo","VesselName" ,"ProjectCode", "FishingArea","LandingPort","LastPortDate","LastTripObsvDate","CrewCount","CrewNationality","CrewList","AuditDate","AuditRef"]) 
                st.dataframe(df)
                cursor.close()
            
            if table == "Vessel Regulatory Body":
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM vesselregulatorybody")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["UVINo", "RFMOType","RegNo","StartDate","EndDate"]) 
                st.dataframe(df)
                cursor.close()
            
            if table == "Project":
                cursor = conn.cursor()
                cursor.execute("""
SELECT 
    sop.*, so.StakeholderName
FROM
    (SELECT 
        `project`.`ProjectCode`,
            `organisation`.`OrgName` AS 'Client',
            `project`.`ProjectType` AS 'Project Type',
            `project`.`ProjectName` AS 'Project Name',
            `project`.`ProjectDescription` AS 'Project Description',
            `project`.`TermsOfReference` AS 'Terms of Reference',
            `project`.`StartDate` AS 'Start Date',
            `project`.`EndDate` AS 'End Date'
    FROM
        `heroku_53bd8d966df0668`.`project`
    INNER JOIN Organisation ON organisation.OrgId = project.ClientId
    LEFT JOIN stakeholder ON stakeholder.ProjectCode = project.ProjectCode) sop
        LEFT JOIN
    (SELECT 
        `stakeholder`.`ProjectCode`,
            `stakeholder`.`StakeholderId`,
            OrgName AS 'StakeholderName'
    FROM
        `heroku_53bd8d966df0668`.`stakeholder`
    INNER JOIN organisation ON organisation.OrgId = stakeholder.StakeholderId) so ON sop.projectcode = so.projectcode""")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["ProjectCode", "Client" ,"ProjectType", "ProjectName", "ProjectDescription", "TermsOfReference", "StartDate", "EndDate","StakeholderName",]) 
                st.dataframe(df)
                cursor.close()

            if table == "Project Team":
                cursor = conn.cursor()
                cursor.execute("""SELECT 
    `projectteam`.`ProjectCode` AS 'Project Code',
    `projectteam`.`ConsultantId` AS 'Consultant Id',
    CONCAT(ConsultantFirstName, ConsultantLastName) AS 'Consultant Name',
    ConsultantDesignation AS 'Consultant Designation',
    `projectteam`.`ProjectRole` AS 'Role',
    `projectteam`.`No_of_Days` AS 'Days Spent'
FROM
    `heroku_53bd8d966df0668`.`projectteam`
        INNER JOIN
    Consultant ON Consultant.ConsultantId = projectteam.ConsultantId""")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["ProjectCode","ConsultantId" ,"ConsultantName","ConsultantDesignation","ProjectRole",  "No_of_Days"]) 
                st.dataframe(df)
                cursor.close()

            if table == "Certification":
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM certification")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["Company","Vessel", "CertificationName", "CertificationNo"])
                st.dataframe(df)
                cursor.close()
                
            elif table == "Certification Type":
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM certificationtype")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["CertificationName","CertificateDescription"])
                st.dataframe(df)
                cursor.close()
                
            elif table == "Consultant":
                cursor = conn.cursor()
                cursor.execute("SELECT ConsultantID, ConsultantType, Pswd,ConsultantFirstName,ConsultantLastName,ConsultantDesignation, ConsultantReviews FROM consultant")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["ConsultantID", "ConsultantType", "Pswd","ConsultantFirstName","ConsultantLastName","ConsultantDesignation", "ConsultantReviews"])
                st.dataframe(df)
                cursor.close()
            elif table == "Stakeholder":
                cursor = conn.cursor()
                cursor.execute("SELECT *FROM stakeholder")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["ProjectCode", "StakeholderId"])
                st.dataframe(df)
                cursor.close()

            elif table == "Country":
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM country")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=["CountryId",  "CountryName"])
                st.dataframe(df)
                cursor.close()

if __name__ == "__main__":
    
    #if login_form():
    main()
