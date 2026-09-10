# Industry data schema

The JSON file is the source of truth. The renderer accepts this shape. Keep analytical context in `orientation` and node details; only real value-chain stages belong in `stages`.

## Top level

```json
{
  "title": "DPU产业链",
  "as_of_date": "2026-09-10",
  "scope": {
    "product": "DPU/IPU基础设施处理器",
    "geography": "全球，重点关注中国",
    "time_horizon": "当前格局与未来3年",
    "company_universe": "上市与未上市公司",
    "included": ["DPU芯片", "板卡", "软件栈", "部署与应用"],
    "excluded": ["普通以太网网卡", "GPU scale-up互连"]
  },
  "orientation": {
    "purpose": "帮助投资实习生建立赛道结构并识别后续尽调重点",
    "lifecycle_stage": "导入期向成长期过渡",
    "lifecycle_basis": "头部云厂商已部署，但第三方商业化和软件生态仍在形成。",
    "demand_state": "AI基础设施扩容拉动需求，采购仍集中在少数大型客户。",
    "market_definition": "只统计DPU/IPU芯片、板卡和直接相关软件收入，不含普通NIC和数据中心服务收入。",
    "key_debates": ["独立DPU厂商能否突破云厂商自研", "软件生态能否形成迁移成本"],
    "source_ids": ["orientation-source"]
  },
  "stages": [],
  "nodes": [],
  "edges": [],
  "sources": []
}
```

`orientation` gives the reader a compact research lens. It is not a substitute for an industry report and its fields must not be rendered as chain stages.

## Stage

```json
{
  "id": "chip",
  "title": "DPU芯片设计",
  "kind": "chain",
  "order": 2,
  "description": "把IP、制造资源和软件能力集成为DPU SoC。"
}
```

`kind` is `chain` for true upstream/downstream stages and `support` for cross-chain capabilities such as software, standards, certification, or distribution. Chain-stage `order` must be unique.

## Node

```json
{
  "id": "foundry",
  "stage_id": "upstream",
  "title": "晶圆制造",
  "summary": "晶圆制造把芯片版图转换为可封装测试的物理晶圆。先进制程影响DPU的性能、功耗与单位成本，良率和产能则直接影响交期。DPU通常只占代工厂需求的一部分，因此节点重要性不等于DPU客户拥有议价权。",
  "chain_role": {
    "inputs": ["芯片版图", "光罩", "晶圆与制造材料"],
    "transformation": "通过光刻、沉积、刻蚀等工序在晶圆上形成集成电路。",
    "outputs": ["完成前道制造的晶圆"],
    "customers": ["DPU芯片设计公司"],
    "payer": "采用Fabless模式的DPU芯片公司"
  },
  "companies": [
    {
      "name": "TSMC",
      "role": "为先进制程芯片提供晶圆代工",
      "geography": "全球",
      "evidence_status": "verified_participant",
      "source_ids": ["tsmc-foundry"]
    }
  ],
  "technology_routes": [
    {
      "name": "先进制程单片SoC",
      "maturity": "已量产",
      "trade_off": "性能与能效较高，但掩膜和流片成本高、产能依赖集中。",
      "adoption_signal": "更多DPU量产型号转向先进节点，并出现持续晶圆订单。",
      "source_ids": ["tsmc-foundry"]
    }
  ],
  "economics": {
    "revenue_model": "按晶圆和工艺服务收费。",
    "cost_drivers": ["折旧", "设备与材料", "良率损失", "能源"],
    "bargaining_power": "先进节点产能集中使代工厂通常强于中小芯片客户。",
    "profit_pool_logic": "工艺领先、良率和稀缺产能支撑较强价值捕获，但DPU贡献需与代工厂整体业务区分。",
    "price_or_capacity_transmission": "晶圆价格、良率和交期变化通过芯片成本与可交付数量传导到板卡和整机。"
  },
  "competition": ["制程能力", "良率", "产能与交期", "成本", "先进封装协同"],
  "metrics": [
    {
      "name": "目标制程节点与量产良率",
      "why_it_matters": "共同决定可销售芯片数量、单位成本和性能功耗。",
      "signal": "良率持续提升且接近成熟产品，通常强化量产经济性。",
      "source_ids": ["tsmc-foundry"]
    },
    {
      "name": "平均交期",
      "why_it_matters": "反映产能紧张程度和客户获得供给的能力。",
      "signal": "交期异常拉长可能限制下游出货并推高库存。",
      "source_ids": ["tsmc-foundry"]
    },
    {
      "name": "先进节点产能利用率",
      "why_it_matters": "影响代工厂议价与新增订单可获得性。",
      "signal": "高利用率强化代工厂议价，但可能挤压中小客户供给。",
      "source_ids": ["tsmc-foundry"]
    }
  ],
  "investment_view": {
    "thesis": "先进制程和良率形成议价权，但DPU通常只是代工厂需求的一小部分。",
    "moat": "工艺、良率、客户认证和资本强度。",
    "catalyst": "DPU进入规模量产并提高先进节点利用。",
    "risk": "需求不及预期、客户集中和资本开支周期。",
    "watch": "DPU相关流片从一次性项目转为持续晶圆订单。"
  },
  "diligence_questions": [
    "DPU订单占目标产能和收入多少？",
    "良率和晶圆价格如何传导到芯片毛利？",
    "订单是试产、首批量产还是可重复采购？"
  ],
  "source_ids": ["tsmc-foundry"]
}
```

The node drawer should deliver roughly 7–12 concise sentences across sections, not one unbroken essay. Nested `source_ids` must also appear in the node's aggregate `source_ids` so the drawer can show all relevant evidence.

### Company evidence status

- `verified_supplier`: a source verifies supply into the mapped chain.
- `verified_customer`: a source verifies purchasing or production use.
- `verified_participant`: a source verifies operation in the node, not a specific supply/customer relationship.
- `reported_poc`: only a test, evaluation, partnership, or PoC is evidenced.
- `representative_target`: representative of the customer type; no adoption claim.
- `inference`: analyst inference that must be clearly labeled.

## Edge

```json
{
  "from": "foundry",
  "to": "dpu-chip",
  "type": "supply",
  "label": "晶圆交付",
  "mechanism": "晶圆价格、良率和交期决定芯片可交付量及单位制造成本；芯片公司再决定吸收或向板卡价格传导。",
  "source_ids": ["tsmc-foundry"]
}
```

Allowed `type` values: `supply`, `product`, `service`, `demand`, and `support`. Direction must match the meaning of the edge. `mechanism` explains how product, price, capacity, lead-time, regulatory, or demand changes move across the relationship.

## Source

```json
{
  "id": "tsmc-foundry",
  "title": "Dedicated IC Foundry",
  "publisher": "TSMC",
  "url": "https://www.tsmc.com/english/dedicatedFoundry",
  "published_date": null,
  "accessed_date": "2026-09-10",
  "source_type": "company_primary",
  "supports": ["晶圆制造定义", "TSMC晶圆代工参与", "节点与下游芯片公司的供应关系"]
}
```

Every `source_id` must resolve to a top-level source. Prefer a page that directly supports the nearby claim rather than a generic corporate homepage. Use consistent ISO dates (`YYYY-MM-DD`).
