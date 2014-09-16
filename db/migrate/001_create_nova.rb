class CreateNova < ActiveRecord::Migration
  def self.up
    create_table :nova do |t|
      t.integer :sid
      t.integer :cid
      t.string :tenantid
      t.string :instanceid
      t.string  :user_email
      t.string :userid
      t.index   :sid
      t.index   :cid
      t.index   :tenantid
      t.index   :instanceid
      t.index   :user_email
      t.index   :userid
    end
  end
  def self.down
    drop_table :novahdr
  end
end
