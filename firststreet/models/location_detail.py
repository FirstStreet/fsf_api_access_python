from firststreet.models.geometry import Geometry


class Zcta:

    def __init__(self, data):
        if data:
            self.fsid = data.get('fsid')
            self.name = data.get('name')

    def __eq__(self, other):
        if not isinstance(other, Zcta):
            return NotImplemented

        super().__eq__(other)

        return self.fsid == other.fsid and self.name == other.name

    def __repr__(self):
        return "<fsid:%s name:%s>" % (self.fsid, self.name)


class Tract:

    def __init__(self, data):
        if data:
            self.fsid = data.get('fsid')
            self.name = data.get('name')

    def __eq__(self, other):
        if not isinstance(other, Tract):
            return NotImplemented

        super().__eq__(other)

        return self.fsid == other.fsid and self.name == other.name

    def __repr__(self):
        return "<fsid:%s name:%s>" % (self.fsid, self.name)


class County:

    def __init__(self, data):
        if data:
            self.fsid = data.get('fsid')
            self.name = data.get('name')

    def __eq__(self, other):
        if not isinstance(other, County):
            return NotImplemented

        super().__eq__(other)

        return self.fsid == other.fsid and self.name == other.name

    def __repr__(self):
        return "<fsid:%s name:%s>" % (self.fsid, self.name)


class Cd:

    def __init__(self, data):
        if data:
            self.fsid = data.get('fsid')
            self.name = data.get('name')

    def __eq__(self, other):
        if not isinstance(other, Cd):
            return NotImplemented

        super().__eq__(other)

        return self.fsid == other.fsid and self.name == other.name

    def __repr__(self):
        return "<fsid:%s name:%s>" % (self.fsid, self.name)


class State:

    def __init__(self, data):
        if data:
            self.fsid = data.get('fsid')
            self.name = data.get('name')

    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented

        super().__eq__(other)

        return self.fsid == other.fsid and self.name == other.name

    def __repr__(self):
        return "<fsid:%s name:%s>" % (self.fsid, self.name)


class Fema:

    def __init__(self, data):
        if data:
            self.femaId = data.get('femaId')
            self.zone = data.get('zone')

    def __eq__(self, other):
        if not isinstance(other, Fema):
            return NotImplemented

        super().__eq__(other)

        return self.femaId == other.femaId and self.zone == other.zone

    def __repr__(self):
        return "<femaId:%s zone:%s>" % (self.femaId, self.zone)


class LocationDetail:

    def __init__(self, response):
        self.fsid = response.get('fsid')
        self.streetNumber = response.get('streetNumber')
        self.route = response.get('route')
        self.city = response.get('city')
        self.lsad = response.get('lsad')
        self.zipCode = response.get('zipCode')
        zcta = response.get('zcta')
        if isinstance(zcta, list):
            self.zcta = [Zcta(zcta_data) for zcta_data in zcta]
        elif isinstance(zcta, dict):
            self.zcta = Zcta(zcta)
        else:
            self.zcta = zcta
        self.neighborhood = response.get('neighborhood')
        self.subtype = response.get('subtype')
        if response.get('tract'):
            self.tract = Tract(response.get('tract'))
        self.fips = response.get('fips')
        county = response.get('county')
        if isinstance(county, list):
            self.county = [County(county_data) for county_data in county]
        elif isinstance(county, dict):
            self.county = County(county)
        else:
            self.county = county
        self.isCoastal = response.get('isCoastal')
        cd = response.get('cd')
        if isinstance(cd, list):
            self.cd = [Cd(cd_data) for cd_data in response.get('cd')]
        elif isinstance(cd, dict):
            self.cd = Cd(response.get('cd'))
        else:
            self.cd = response.get('cd')
        self.congress = response.get('congress')
        if response.get('state'):
            self.state = State(response.get('state'))
        self.footprintId = response.get('footprintId')
        self.elevation = response.get('elevation')
        fema = response.get('fema')
        if isinstance(fema, list):
            self.fema = [Fema(fema_data) for fema_data in fema]
        elif isinstance(fema, dict):
            self.fema = Fema(fema)
        else:
            self.fema = fema
        if response.get('geometry'):
            self.geometry = Geometry(response.get('geometry'))
        self.name = response.get('name')
        self.district = response.get('district')
