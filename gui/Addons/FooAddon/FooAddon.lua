-- First, we create a namespace for our addon by declaring a top-level table that will hold everything else.
FooAddon = {}

-- This isn't strictly necessary, but we'll use this string later when registering events.
-- Better to define it in a single place rather than retyping the same string.
FooAddon.name = "FooAddon"

function FooAddon.OnIndicatorMoveStop()
    FooAddon.savedVariables.left = FooAddonIndicator:GetLeft()
    FooAddon.savedVariables.top = FooAddonIndicator:GetTop()
end

function FooAddon:RestorePosition()
    local left = self.savedVariables.left
    local top = self.savedVariables.top
   
    FooAddonIndicator:ClearAnchors()
    FooAddonIndicator:SetAnchor(TOPLEFT, GuiRoot, TOPLEFT, left, top)
end
      
function AddonOnUpdate()
    if(gps ~= nil) then
        local x, y, zoneMapIndex = gps:LocalToGlobal(GetMapPlayerPosition("player"))
        local angle = (math.deg(GetPlayerCameraHeading())-180) % 360
        FooAddonIndicatorLabel:SetText(string.format("%f : %f : %d", x, y, angle))
    end
end

-- Next we create a function that will initialize our addon
function FooAddon:Initialize()

    gps = LibStub("LibGPS2")

    -- ...but we don't have anything to initialize yet. We'll come back to this.
    self.savedVariables = ZO_SavedVars:New("FooAddonSavedVariables", 1, nil, {})
    self:RestorePosition()
end

-- Then we create an event handler function which will be called when the "addon loaded" event
-- occurs. We'll use this to initialize our addon after all of its resources are fully loaded.
function FooAddon.OnAddOnLoaded(event, addonName)
    -- The event fires each time *any* addon loads - but we only care about when our own addon loads.
    if addonName == FooAddon.name then
        FooAddon:Initialize()
    end
end
    
-- Finally, we'll register our event handler function to be called when the proper event occurs.
EVENT_MANAGER:RegisterForEvent(FooAddon.name, EVENT_ADD_ON_LOADED, FooAddon.OnAddOnLoaded)