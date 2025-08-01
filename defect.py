import os
import streamlit as st 
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

from PIL import Image # pillow is used to load, save and manipulate the image 

st.set_page_config(page_title='Defect Detection',page_icon='👨🏻‍💻',layout='wide')

st.title('Ai Assistant for :green[Structural Defect and Analysis]')
st.subheader(':blue[Prototype for automated structural defect analysis]',divider=True)

with st.expander('About the application:'):
    st.markdown(f'''This prototype is used to detect the structural defects and analyze the 
                defects using AI- powered system.
                - **Defect Detection** : Automatically detects the structural defects in the given images like cracks, misalignments.
                - **Recommendations** : Provides solution and recommendations based on the defects
                - **Report Generation** : Create a detailed report for the documentation and future purpose.
                ''')
    
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)

st.subheader('Upload image here')
input_image = st.file_uploader('Upload the image here',type=['png','jpg','jpeg'])

img=''
if input_image:
    img = Image.open(input_image)
    st.image(img, caption='Uploaded image')



prompt = f'''Act as a structural and civil engineer and provide the neccessary details in
proper bullet points in more precise way ( maximum 3 lines ) and answer for the following questions:

1. Is there is any structural defects such as cracks, bends, damage in the given image and give the probability?
2. What is the severity level of the defect like minor, moderate or major defcts
3. What is the possible cause for the given defect, considering the material damage, environmental damage
4. Under what condition the defect shown will propage further in future?
5. Say whether we can repair this defect or not? If not say whether we need to replace this or not?
6. Suggest the remedies to repair the defect caused including materials used to repair the defect.
7. Say whether the defect shown with affect the surroungings and give probability for that.
8. Say whether we need to monitor the defected area after repair or replacements.
9. Dose the observed defect has any dependency on indusries.
10. What are the possibilities for teh defects to happen again?

'''



def generate_results(prompt,input_image):
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    result = model.generate_content(f'''Using the given prompt {prompt} analyze 
                                    the given image {img} and generate the results based
                                     on the prompt''')
    return result.text

submit = st.button('Analyze the defect')

if submit:
    with st.spinner('Analyzing.....'):
        response = generate_results(prompt,img)
        
        st.markdown('## :green[Results]')
        st.write(response)