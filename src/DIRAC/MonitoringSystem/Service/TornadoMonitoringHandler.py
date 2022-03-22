""" Tornado-based HTTPs Monitoring service.

.. literalinclude:: ../ConfigTemplate.cfg
  :start-after: ##BEGIN TornadoMonitoring
  :end-before: ##END
  :dedent: 2
  :caption: Monitoring options

"""
from base64 import b64encode

from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC.Core.Tornado.Server.TornadoService import TornadoService
from DIRAC.Core.Utilities.Plotting import gDataCache
from DIRAC.Core.Utilities.Plotting.Plots import generateErrorMessagePlot
from DIRAC.MonitoringSystem.Service.MonitoringHandler import MonitoringHandlerMixin


sLog = gLogger.getSubLogger(__name__)


class TornadoMonitoringHandler(MonitoringHandlerMixin, TornadoService):
    log = sLog

    types_streamToClient = []

    def export_streamToClient(self, fileId):
        """
        Get graphs data

        :param str fileId: encoded plot attributes
        """

        # First check if we've got to generate the plot
        if len(fileId) > 5 and fileId[1] == ":":
            self.log.info("Seems the file request is a plot generation request!")
            try:
                result = self._generatePlotFromFileId(fileId)
            except Exception as e:  # pylint: disable=broad-except
                self.log.exception("Exception while generating plot", str(e))
                result = S_ERROR("Error while generating plot: %s" % str(e))
            if not result["OK"]:
                return S_OK(b64encode(generateErrorMessagePlot(result["Message"])).decode())
            fileId = result["Value"]

        retVal = gDataCache.getPlotData(fileId)
        if not retVal["OK"]:
            return S_OK(b64encode(generateErrorMessagePlot(result["Message"])).decode())
        return S_OK(b64encode(retVal["Value"]).decode())
