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
                       |       |        |        ^
                 reorders  reads_stock  plans     |
                       |       |        |   reports_shipped
                       v       v        v         |
              +---------+ +-----------+ +------------+ +--------------+
              | Supply  | | Inventory | | Production | | Fulfillment  |
              +---------+ +-----------+ +------------+ +--------------+

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

## Cross-source edges

The 30 edges below are the machine-checked cross-source edges from
`eval/_cross_source/structure.yaml` — every edge whose two endpoints are
owned by different areas, regardless of tier. This list is hand-maintained;
keep it in sync with `eval/_cross_source/structure.yaml`.

- Planning & Demand --reorders--> Supply (tier 0)
- Planning & Demand --plans--> Production (tier 0)
- Planning & Demand --reads_stock--> Inventory (tier 0)
- Supply --posts_cost--> Finance (tier 0)
- Production --posts_cost--> Finance (tier 0)
- Fulfillment --posts_cost--> Finance (tier 0)
- Fulfillment --reports_shipped--> Planning & Demand (tier 0)
- Planner --reads_stock--> PartsDB (tier 1)
- Planner --plans_build--> Assembly (tier 1)
- Planner --reorders--> Procurement (tier 1)
- City Cruiser Order --fulfilled_by--> City Cruiser Shipment (tier 2)
- Trail Blazer Order --fulfilled_by--> Trail Blazer Shipment (tier 2)
- Frame Stock --tracks--> Frame (tier 2)
- Wheelset Stock --tracks--> Wheelset (tier 2)
- Drivetrain Stock --tracks--> Drivetrain (tier 2)
- Brake Set Stock --tracks--> Brake Set (tier 2)
- Suspension Fork Stock --tracks--> Suspension Fork (tier 2)
- City Cruiser --uses--> Frame (tier 2)
- City Cruiser --uses--> Wheelset (tier 2)
- City Cruiser --uses--> Drivetrain (tier 2)
- City Cruiser --uses--> Brake Set (tier 2)
- Trail Blazer --uses--> Frame (tier 2)
- Trail Blazer --uses--> Wheelset (tier 2)
- Trail Blazer --uses--> Suspension Fork (tier 2)
- City Cruiser Shipment --ships--> City Cruiser (tier 2)
- Trail Blazer Shipment --ships--> Trail Blazer (tier 2)
- Procurement --posts--> Purchase Cost (tier 2)
- Assembly --posts--> Labor Cost (tier 2)
- Quality --posts--> Scrap Cost (tier 2)
- Shipping --posts--> Freight Cost (tier 2)
