# Modules

Each module is accessed as an attribute on `HelldiveAPIClient` and handles one API resource group. All modules share the same pattern: `get_all()` returns a list, `get(index)` returns a single item or `None` on 404, and non-404 HTTP errors are re-raised.

::: helldivepy.modules.war.WarModule

::: helldivepy.modules.dispatches.DispatchesModule

::: helldivepy.modules.planets.PlanetModule

::: helldivepy.modules.campaigns.CampaignModule

::: helldivepy.modules.assignments.AssignmentsModule

::: helldivepy.modules.space_stations.SpaceStationsModule

::: helldivepy.modules.steam.SteamModule
