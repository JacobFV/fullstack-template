- for each model:
  - set exclude=True and private=True on all db/read fields that are not meant to be returned to the user
  - set frozen=True on all db fields that are not meant to be updated after initialization
  - set exclude on relationship fields to make sure we are only returning the minimum connected nested field values on read, otherwise we could end up with cyclic deps during quiery JSONification
  - put the other schema deps in an if TYPE_CHECKING enclosure so we can keep the imports clean
  - move all crud routers to their api files
  - set view_privileges and update_privileges on all relevant fields
- global context object instead of user/session/etc contexts
- OpenAPI Spec
- unit tests (find an AI to write, run, and debug)

Field configs by class:

- **Base**
  - pull all common fields from the model
- **Create**
  - just make sure it's ok :)
- **Read**
  - do not include `ModelRead` fields in the read schema. Those should be read separately unless you absolutely have to. Otherwise, just keep ID.
  - set `schema_extras={ModelRead.PRIVILEGES_KEY: ModelRead.Privileges.<option>}` to control the read privileges
- **Update**
  - do not include `ModelUpdate` fields in the update schema. Those should be updated separately. Only keep ID.
  - set `schema_extras={ModelUpdate.PRIVILEGES_KEY: ModelUpdate.Privileges.<option>}` to control the update privileges
- **InDB**
  - set `exclude=True` on all exceptionally important fields that should never be returned under any circumstance. (the Read variant schema already does this for all the fields, just added protection)
  - set `frozen=True` on all db exceptionally important fields that are not meant to be updated after initialization. (the Update variant schema already does this for all the fields, just added protection)

### TODOs

[*] refactor HasOwner into the schema inheritance tree
[*] set the DEFAULT_PRIVILEGES on all read and update models
[*] ensure all models override from_create, update_from, and to_read to match the new interface in ModelInDB
[ ] make all users a sub of User. use field unions instead of separate classes for complex operations (excluding develop accounts):
  - eg, for_browser_instance_with_token or for_email can be set as validation
[ ] move all crud routers to their api files
[ ] make a post-init file what i update forward refs for all models since i chase one
[ ] global context object instead of user/session/etc contexts
[ ] OpenAPI Spec
[ ] unit tests (find an AI to write, run, and debug)
