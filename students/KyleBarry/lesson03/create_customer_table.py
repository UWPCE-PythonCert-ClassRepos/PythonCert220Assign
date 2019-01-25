import customer_model as cm

cm.database.create_tables([cm.Customer])
cm.database.close()
