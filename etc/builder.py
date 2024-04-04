from iocbuilder import AutoSubstitution
from iocbuilder.arginfo import *

from iocbuilder.modules.ADCore import makeTemplateInstance
from iocbuilder.modules.ADGenICam import GenICam

class aravisCameraTemplate(AutoSubstitution):
    TemplateFile="aravisCamera.template"

class aravisCamera(GenICam):
    '''Creates a aravisCamera camera areaDetector driver'''
    Dependencies = (GenICam,)
    # This tells xmlbuilder to use PORT instead of name as the row ID
    UniqueName = "PORT"
    _SpecificTemplate = aravisCameraTemplate
    # List of camera classes available from ADGenICam
    camera_class_list = [
        'AVT_Mako_1_52',
        'AVT_Mako_G040B',
        'AVT_Mako_G125B',
        'AVT_Mako_G125C',
        'AVT_Mako_G158B',
        'AVT_Mako_G158C',
        'AVT_Mako_G234B',
        'AVT_Mako_G234C',
        'AVT_Mako_G319C',
        'AVT_Mako_G507B',
        'AVT_Mako_G507C',
        'AVT_Mako_G511C',
        'AVT_Manta_1_44',
        'AVT_Manta_G040B',
        'AVT_Manta_G125B',
        'AVT_Manta_G125C',
        'AVT_Manta_G145B',
        'AVT_Manta_G235B',
        'AVT_Manta_G235C',
        'AVT_Manta_G319B',
        'AVT_Manta_G419C',
        'AVT_Manta_G507B',
        'AVT_Manta_G609B',
        'AVT_Manta_G895B',
        'AVT_Manta_G895C',
        'AVT_Manta_G2460C',
        'AVT_Prosilica_GC655C',
        'AVT_Prosilica_GC1020C',
        'AVT_Prosilica_GC1280M',
        'AVT_Prosilica_GT5120',
        'Prosilica_GC',
        'Basler_piA640_210gm',
        'JAI_CM140',
        'JAI_CM140_v2-2',
        'JAI_GO5000MPGE1',
        'XIMEA_MC124CG-SY'
    ]
    def __init__(self, P, R, PORT, ID, CLASS, PV_ALIAS, BUFFERS=50, MEMORY=-1, **args):
        # Init the superclass
        self.__super.__init__(P, R, PORT, ID, CLASS, BUFFERS, MEMORY)
        # Update the attributes of self from the commandline args
        self.__dict__.update(locals())
        # Make an instance of our template
        makeTemplateInstance(self._SpecificTemplate, locals(), args)
        # Backwards compatible Manta
        # Init the camera specific class


        class _alias(AutoSubstitution):
            ModuleName = aravisCamera.ModuleName
            TemplateFile = "PVAlias.template"

        if PV_ALIAS > 0:
            makeTemplateInstance(_alias, locals(), args)

    # __init__ arguments
    ArgInfo = makeArgInfo(__init__,
        P       = Simple('PV Prefix', str),
        R       = Simple('PV Suffix', str),
        PORT    = Simple('Port name for the camera', str),
        ID      = Simple('Cam ip address, hostname, MAC address, or ID <manufacturer>-<serial>, (e.g. Prosilica-02-2166A-06844)', str),
        CLASS   = Choice('Camera class for custom commands', camera_class_list),
        PV_ALIAS= Choice('Use alias template to keep some key PV names the same',
            [0,1]),
        BUFFERS = Simple('Maximum number of NDArray buffers to be created for '
            'plugin callbacks', int),
        MEMORY  = Simple('Max memory to allocate, should be maxw*maxh*nbuffer '
            'for driver and all attached plugins', int))


    def Initialise(self):
        #print "aravisConfig(const char *portName, const char *cameraName, size_t maxMemory, int priority, int stackSize)"
        print 'aravisConfig("%(PORT)s", "%(ID)s", %(MEMORY)d, 0, 1)' % self.__dict__

    # Device attributes
    LibFileList = ['ADAravis']
    DbdFileList = ['ADAravisSupport']



