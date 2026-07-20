# Labs 目录

> `vertical/`、旧键盘页面及旧测试页保留为历史实验，其中可能包含已经
> 证伪的 `text-orientation: upright` 或旋转方案。它们不得作为正式实现；
> 正式竖排入口统一使用 `core/mongolian_layout_engine.*`。

除 `input/ai-chat.html` 外，本目录中的页面均为历史实验，不代表当前正式产品能力或质量承诺。

## 正式 Alpha

- `input/ai-chat.html`：传统蒙古文输入、原生竖排与基础规则响应。

## Labs 分类

- `keyboard/`：不同虚拟键盘布局实验。
- `vertical/`：CSS、SVG 与历史旋转方案的渲染实验。
- `input/`：早期聊天、输入法与移动布局原型。
- `tests/`：人工打开的展示型测试页，不等同于自动化测试。

自动化回归测试位于仓库根目录的 `tests/`。历史页面可能包含已知错误、过时文案或不符合当前无障碍基线的实现；如需复用，请先迁移到当前正式页面的组件与安全模式。
