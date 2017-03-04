"""Model static set of objects, pools, and meta pools for testing."""

# Twisted Imports
from twisted.internet import defer

# Zenoss Imports
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap


class AggLap(PythonPlugin):
    def collect(self, device, log):
        log.info("%s: faking data for %s", self.name(), device.id)

        metapools_rm = RelationshipMap(relname="aggLapMetaPools")
        pools_rm = RelationshipMap(relname="aggLapPools")
        objects_rm = RelationshipMap(relname="aggLapObjects")

        for metapool_idx in range(1, 2):
            metapools_rm.append(
                ObjectMap(
                    modname="ZenPacks.test.AggLap.AggLapMetaPool",
                    data={
                        "id": "metapool-{}".format(metapool_idx),
                        "title": "Meta Pool {}".format(metapool_idx),
                        }))

            for pool_idx in range(1, 3):
                pools_rm.append(
                    ObjectMap(
                        modname="ZenPacks.test.AggLap.AggLapPool",
                        data={
                            "id": "pool-{}-{}".format(metapool_idx, pool_idx),
                            "title": "Pool {}/{}".format(metapool_idx, pool_idx),
                            "set_aggLapMetaPool": "metapool-{}".format(metapool_idx),
                            }))

                for object_idx in range(1, 3):
                    objects_rm.append(
                        ObjectMap(
                            modname="ZenPacks.test.AggLap.AggLapObject",
                            data={
                                "id": "object-{}-{}-{}".format(metapool_idx, pool_idx, object_idx),
                                "title": "Object {}/{}/{}".format(metapool_idx, pool_idx, object_idx),
                                "set_aggLapPool": "pool-{}-{}".format(metapool_idx, pool_idx),
                                }))

        return defer.succeed([metapools_rm, pools_rm, objects_rm])

    def process(self, device, results, log):
        log.info("%s: processing data from %s", self.name(), device.id)
        return results
