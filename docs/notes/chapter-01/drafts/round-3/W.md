## modelVsRealityOwner

The lab's warehouse records the owning account and models no such rights. In some real databases, a table's owner is an account too. In PostgreSQL, for example, a new table's owner is normally the account that created it. At first, only the owner (or a superuser) can do anything with the table. Other accounts can use it once they are given the right to. The right to alter or drop the table comes with being its owner.
