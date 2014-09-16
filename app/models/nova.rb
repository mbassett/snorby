class Nova
  include DataMapper::Resource

  storage_names[:default] = "novahdr"

  belongs_to :sensor, :parent_key => [ :sid ], :child_key => [ :sid ], :required => true

  belongs_to :event,
             :parent_key => [ :sid, :cid ],
             :child_key => [ :sid, :cid ],
             :required => true

  property :sid, Integer, :key => true, :index => true, :min => 0

  property :cid, Integer, :key => true, :index => true, :min => 0

  property :tenantid, String, :index => true
  
  property :instanceid, String, :index => true

  property :user_email, String, :index => true

  property :userid, String, :index => true

end
