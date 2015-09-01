"""A smart video is a kaltura video that will get a single video based on a query
   The best example is the most recent video in a specific category
   As a content type, you can create a smart video and slot it as a promo on a portal page.
"""
from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes import atapi

from rfa.kaltura import kutils
from rfa.kaltura.content import base as KalturaBase
from rfa.kaltura.interfaces import IKalturaSmartVideo
from rfa.kaltura.config import PROJECTNAME

SmartVideoSchema = KalturaBase.KalturaBaseSchema.copy() + \
                   KalturaBase.KalturaMetadataSchema.copy() + \
                   ATContentTypeSchema.copy()

SmartVideoSchema['categories'].widget.description = "Select category to choose most recent category from"
SmartVideoSchema['categories'].widget.description_msgid="desc_svideo_categories"
SmartVideoSchema["entryId"].widget.description = "Entry ID of video that will be returned"
SmartVideoSchema["tags"].widget.visible = {"edit": "invisible"}


finalizeATCTSchema(SmartVideoSchema, moveDiscussion=False)

from zope.interface import Interface

class KalturaSmartVideo(base.ATCTContent, KalturaBase.KalturaContentMixin):
    
    implements(IKalturaSmartVideo)
    meta_type = "KalturaSmartVideo"
    schema = SmartVideoSchema
    
    security = ClassSecurityInfo()
        
    security.declarePrivate('getDefaultPlayerId')
    def getDefaultPlayerId(self):
        return "20100652" #todo - add to config

    
    def dynamicKalturaObject(self):
        
        catFilter = kutils.makeFilter(catIds=self.categories.keys())
        vidlist = kutils.getRecent(limit=1, partner_id=self.partnerId, filt=catFilter)
        
        try:
            self._cachedKalturaObject = vidlist[0]
        except IndexError:
            self._cachedKalturaObject = None
    
        return self._cachedKalturaObject
        
    KalturaObject = property(dynamicKalturaObject) 
        
        
atapi.registerType(KalturaSmartVideo, PROJECTNAME)