# PedalWorks — architecture flow

PedalWorks is organized around six themes, and this page is the map of how
they hand work and money to one another. Everything else in `docs/` zooms
into one theme at a time; this page is the only place that steps back and
shows all six at once.

The six themes are **Planning & Demand**, **Supply**, **Inventory**,
**Production**, **Fulfillment**, and **Finance**. Planning & Demand is where
customer demand turns into action: it is the theme that decides what needs
to happen next, and it drives the other themes rather than being driven by
them. Supply is everything to do with getting parts from outside suppliers
into the building. Inventory is where those parts are tracked once they have
arrived. Production is where parts become finished bicycles. Fulfillment is
getting a finished bicycle from the building to the customer who ordered it.
Finance is where every theme's spending ends up, regardless of which theme
generated it.

## How the themes connect

```
                        +-----------------------+
                        |   Planning & Demand    |
                        +-----------------------+
                           |        |        ^
                     reorders   reads_stock  |
                           |        |    reports_shipped
                           v        v        |
              +---------+   +-----------+   +--------------+
              | Supply  |   | Inventory |   | Fulfillment  |
              +---------+   +-----------+   +--------------+
                   |                              ^
                   |         plans                |
                   +----> Planning & Demand -------+
                           |
                           v
                     +------------+
                     | Production |
                     +------------+

              Supply, Production, and Fulfillment each
                        posts_cost
                            |
                            v
                       +----------+
                       | Finance  |
                       +----------+
```

Planning & Demand reaches out in two directions on the read side and one on
the write side: it reorders Supply when parts are needed, it plans Production
so that assembly work gets released, and it reads stock from Inventory to
know what is actually on hand before it decides either of those things.
Fulfillment closes the loop by reporting back to Planning & Demand once a
bicycle has shipped, so demand and the record of what has actually gone out
the door stay in sync.

Money flows on a separate, simpler path. Supply, Production, and Fulfillment
each post a cost to Finance as they do their work — Finance does not reach
into any of them, it simply receives what they send. Inventory is the one
theme that never posts anything to Finance: it only observes and reports on
stock, it never itself spends money.

## Reading the rest of the docs

Each theme has its own home document with the detail this page deliberately
leaves out — `docs/procurement.md` and `docs/bom.md` for Supply,
`docs/inventory.md` for Inventory, `docs/planning_and_demand.md` for Planning
& Demand, `docs/production.md` for Production, `docs/fulfillment.md` for
Fulfillment, and `docs/finance.md` for Finance. `docs/data-model.md` covers
the systems (`OrderDB`, `PartsDB`, `LedgerDB`) that those themes read and
write.
