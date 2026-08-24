(() => {
    const status = document.querySelector("#render-status");
    const output = document.querySelector("#deterministic-output");
    let settled = false;

    function showFailure(message) {
        if (settled) return;
        settled = true;
        status.textContent = "引擎资源加载失败";
        status.className = "status blocked";
        output.textContent = message;
    }

    window.addEventListener("mongol-engine-ready", () => { settled = true; }, { once: true });
    window.addEventListener("mongol-engine-failed", (event) => {
        showFailure(event.detail || "引擎初始化失败，请刷新页面或查看发布状态。")
    }, { once: true });
    window.addEventListener("error", (event) => {
        if (event.target instanceof HTMLScriptElement) {
            showFailure("浏览器未能加载蒙古文引擎模块。该故障不是输入法问题，请报告当前页面地址。")
        }
    }, true);

    window.setTimeout(() => {
        if (!settled && status.textContent === "引擎加载中") {
            showFailure("蒙古文引擎加载超时，请刷新页面；若仍失败，请报告当前页面地址。")
        }
    }, 30000);
})();
