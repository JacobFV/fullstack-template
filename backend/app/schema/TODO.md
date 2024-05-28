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
  - set `schema_extras={ModelRead.READ_PRIVILEGES_KEY: ModelRead.ReadPrivileges.<option>}` to control the read privileges
- **Update**
  - do not include `ModelUpdate` fields in the update schema. Those should be updated separately. Only keep ID.
  - set `schema_extras={ModelUpdate.UPDATE_PRIVILEGES_KEY: ModelUpdate.UpdatePrivileges.<option>}` to control the update privileges
- **InDB**
  - set `exclude=True` on all fields that should never be returned under any circumstance
  - set `frozen=True` on all db fields that are not meant to be updated after initialization
