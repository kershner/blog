import win32com.client

olMailItem = 0x0
obj = win32com.client.Dispatch("Outlook.Application")
newMail = obj.CreateItem(olMailItem)
newMail.GetInspector()
newMail.Subject = "Subject"
newMail.Body = "Actualemail"
newMail.To = "full@e.mail"
newMail.Attachments.Add("E:\zapp.doc")

newMail.Display()