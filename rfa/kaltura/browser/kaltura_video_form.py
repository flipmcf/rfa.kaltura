"""Private, Authenticated views for Kaltura Videos (edit rights)"""

from zope.interface import Interface
from zope import schema
from zope.i18nmessageid import MessageFactory

from z3c.form import button
from z3c.form import form, field
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from Products.statusmessages.interfaces import IStatusMessage

_ = MessageFactory('kaltura_video')

class IKalturaVideoForm(Interface):    
    title = schema.TextLine(title=_(u'Title'), 
                            required=False)
    description = schema.Text(title=u'Description', 
                              required=False)
    filename = schema.TextLine(title=u'Filename')  
    url = schema.TextLine(title=u'URL', readonly=True)
    
from zope.schema.vocabulary import SimpleVocabulary #XXX Temporary until vocabulary can be moved to proper place
class IKalturaDistributeVideoForm(Interface):
    distChannels = schema.Choice(title=_(u'Choose Distribution Channel'),
                               required=True,
                               vocabulary=SimpleVocabulary.fromValues([u'foo',u'bar']),
                            )
    
    
    


class KalturaVideoForm(form.Form):
    fields = field.Fields(IKalturaVideoForm)
    ignoreContext = True
    
    def updateWidgets(self):
        super(KalturaVideoForm, self).updateWidgets()

    @button.buttonAndHandler(u'Save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        
        if data['title'] is not None:
            title = data['title']
        else:
            title = ''
            IStatusMessage(self.request).addStatusMessage("you got away with not adding a title")
            
        if data['description'] is not None:
            description = data['description']
        else:
            description = ''
            
        if data['filename'] is not None:
            filename = data['filename']
            IStatusMessage(self.request).addStatusMessage("I would have uploaded %s" % (filename,), 'info')
        else:
            filename = 'empty'
            IStatusMessage(self.request).addStatusMessage("you got away with not adding a filename!", 'info')
            
            
        IStatusMessage(self.request).addStatusMessage(
                "Video Saved",
                'info')
        
        redirect_url = "%s/@@kaltura_video_form" % self.context.absolute_url()
        self.request.response.redirect(redirect_url)    


    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            "Canceled",
            'info')
        redirect_url = "%s/@@kaltura_video_form" % self.context.absolute_url()
        self.request.response.redirect(redirect_url)    
        
class KalturaDistributeVideoForm(form.Form):
    fields = field.Fields(IKalturaDistributeVideoForm)
    ignoreContext=True
    
    fields['distChannels'].widgetFactory = CheckBoxFieldWidget
    
    def updateWidgets(self):
        super(KalturaDistributeVideoForm, self).updateWidgets()
        
    @button.buttonAndHandler(u'Save')
    def handleSave(self, action):
        pass
    
    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        pass
        
from plone.z3cform.layout import wrap_form
KalturaVideoFormView = wrap_form(KalturaVideoForm)
DistributeFormView = wrap_form(KalturaDistributeVideoForm)
