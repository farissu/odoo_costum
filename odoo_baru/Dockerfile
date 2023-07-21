FROM odoo:16

# If you have to install from pip and using Odoo >= 11.0
USER root
ENV PATH="/var/lib/odoo/.local/bin:${PATH}"
RUN pip3 install wheel
RUN pip3 install whois
RUN pip3 install supabase
RUN pip3 install xlsxwriter
RUN pip3 install xlrd
RUN pip3 install rsa
RUN pip3 install pandas
RUN pip3 install python-whois
RUN pip3 install cryptography
RUN pip3 install pycryptodome
RUN pip3 install midtransclient
RUN pip3 install oauthlib pyjwt gcloud google-cloud-storage bs4 pydrive instagram_private_api midtransclient
USER odoo