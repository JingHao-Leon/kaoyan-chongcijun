/* Small, self-contained visual labs for 408 chapters. */
(function () {
  function mountCacheLab() {
    var chapter = document.getElementById('3');
    if (!chapter || document.querySelector('.cache-lab')) return;
    var lab = document.createElement('section');
    lab.className = 'interactive-lab cache-lab';
    lab.innerHTML = '<div class="lab-heading"><span>可交互可视化</span><h3>Cache 地址映射模拟器</h3><p>输入主存地址、块大小和 Cache 行数，观察地址如何拆分为 Tag / 行号 / 块内地址。</p></div><div class="lab-controls"><label>主存地址（十六进制）<input data-address value="0x1A3C" inputmode="text"></label><label>块大小（B）<select data-block><option>16</option><option>32</option><option selected>64</option><option>128</option></select></label><label>Cache 行数<select data-lines><option>4</option><option>8</option><option selected>16</option><option>32</option></select></label></div><div class="address-bar"><div><b>Tag</b><span data-tag>—</span></div><div><b>行号 Index</b><span data-index>—</span></div><div><b>块内 Offset</b><span data-offset>—</span></div></div><p class="lab-result" data-result></p>';
    chapter.insertAdjacentElement('afterend', lab);
    var address = lab.querySelector('[data-address]');
    var block = lab.querySelector('[data-block]');
    var lines = lab.querySelector('[data-lines]');
    function powerBits(n) { return Math.log2(n); }
    function update() {
      var value = Number.parseInt(address.value.trim().replace(/^0x/i, ''), 16);
      var blockSize = Number(block.value), lineCount = Number(lines.value);
      if (!Number.isFinite(value) || value < 0) { lab.querySelector('[data-result]').textContent = '请输入非负十六进制地址，例如 0x1A3C。'; return; }
      var memoryBlock = Math.floor(value / blockSize);
      var offset = value % blockSize;
      var index = memoryBlock % lineCount;
      var tag = Math.floor(memoryBlock / lineCount);
      lab.querySelector('[data-tag]').textContent = tag + '（' + tag.toString(2) + '₂）';
      lab.querySelector('[data-index]').textContent = index + '（' + powerBits(lineCount) + ' 位）';
      lab.querySelector('[data-offset]').textContent = offset + '（' + powerBits(blockSize) + ' 位）';
      lab.querySelector('[data-result]').textContent = '地址 ' + address.value.toUpperCase() + ' → 主存块 ' + memoryBlock + ' → 映射到 Cache 第 ' + index + ' 行；Tag 为 ' + tag + '。';
    }
    [address, block, lines].forEach(function (el) { el.addEventListener('input', update); el.addEventListener('change', update); });
    update();
  }

  function mountNetworkLab() {
    var chapter = document.getElementById('1');
    if (!chapter || document.querySelector('.network-lab')) return;
    var lab = document.createElement('section');
    lab.className = 'interactive-lab network-lab';
    lab.innerHTML = '<div class="lab-heading"><span>可交互可视化</span><h3>数据封装路径演示器</h3><p>输入一条应用消息，点击演示，观察它在 TCP/IP 各层中的名称与附加控制信息。</p></div><div class="lab-controls"><label>应用消息<input data-message value="GET /index.html" maxlength="42"></label><button type="button" data-run>演示封装</button></div><div class="network-steps" data-steps></div><p class="lab-result" data-result></p>';
    chapter.insertAdjacentElement('afterend', lab);
    var layers = [
      ['应用层', 'Message', '应用数据'],
      ['运输层', 'Segment', 'TCP/UDP 首部 + 应用数据'],
      ['网络层', 'Packet', 'IP 首部 + 报文段'],
      ['数据链路层', 'Frame', 'MAC 首尾字段 + 分组'],
      ['物理层', 'Bits', '0101… 比特流']
    ];
    function render() {
      var msg = lab.querySelector('[data-message]').value.trim() || '应用消息';
      lab.querySelector('[data-steps]').innerHTML = layers.map(function (item, i) {
        return '<article class="network-step" style="--i:' + i + '"><span>' + (i + 1) + '</span><strong>' + item[0] + '</strong><b>' + item[1] + '</b><p>' + item[2] + '</p></article>';
      }).join('');
      lab.querySelector('[data-result]').textContent = '“' + msg + '” 已从应用层逐层封装，在线路上传输时以 Bits 形式出现；接收端按相反顺序解封装。';
    }
    lab.querySelector('[data-run]').addEventListener('click', render);
    lab.querySelector('[data-message]').addEventListener('input', render);
    render();
  }

  function mountStackLab() {
    var chapter = document.getElementById('3');
    if (!chapter || document.querySelector('.stack-lab')) return;
    var lab = document.createElement('section');
    lab.className = 'interactive-lab stack-lab';
    lab.innerHTML = '<div class="lab-heading"><span>可交互可视化</span><h3>栈操作演示器</h3><p>输入元素并执行入栈或出栈，观察“后进先出（LIFO）”的栈顶变化。</p></div><div class="lab-controls"><label>元素<input data-value value="A" maxlength="4"></label><button type="button" data-push>入栈</button><button type="button" data-pop>出栈</button></div><div class="stack-visual" data-stack></div><p class="lab-result" data-result>当前为空栈。</p>';
    chapter.insertAdjacentElement('afterend', lab);
    var stack = [];
    function render(message) {
      lab.querySelector('[data-stack]').innerHTML = stack.length ? stack.slice().reverse().map(function (item, i) {
        return '<span class="stack-item">' + item.replace(/[<>&]/g, '') + (i === 0 ? '<b>TOP</b>' : '') + '</span>';
      }).join('') : '<em>空栈</em>';
      lab.querySelector('[data-result]').textContent = message || (stack.length ? '栈顶为 ' + stack[stack.length - 1] + '；下一次出栈将先取出它。' : '当前为空栈。');
    }
    lab.querySelector('[data-push]').addEventListener('click', function () {
      var value = lab.querySelector('[data-value]').value.trim() || 'A';
      stack.push(value); render('已将 ' + value + ' 入栈。');
    });
    lab.querySelector('[data-pop]').addEventListener('click', function () {
      render(stack.length ? '已出栈：' + stack.pop() + '。' : '栈为空，不能出栈。');
    });
    render();
  }

  function mountSortLab() {
    var chapter = document.getElementById('7');
    if (!chapter || document.querySelector('.sort-lab')) return;
    var lab = document.createElement('section');
    lab.className = 'interactive-lab sort-lab';
    lab.innerHTML = '<div class="lab-heading"><span>可交互可视化</span><h3>冒泡排序过程演示</h3><p>逐趟查看相邻元素比较、交换和有序区扩张；适合对应“趟数、比较次数、稳定性”类题目。</p></div><div class="lab-controls"><label>待排序序列（逗号分隔）<input data-values value="7,3,5,2,6"></label><button type="button" data-reset>重新开始</button><button type="button" data-next>执行下一趟</button></div><div class="sort-bars" data-bars></div><div class="sort-state" data-state></div><p class="lab-result" data-result></p>';
    chapter.insertAdjacentElement('afterend', lab);
    var values = [], pass = 0;
    function readValues() {
      var parsed = lab.querySelector('[data-values]').value.split(',').map(function (item) { return Number(item.trim()); }).filter(function (n) { return Number.isFinite(n); }).slice(0, 8);
      return parsed.length > 1 ? parsed : [7, 3, 5, 2, 6];
    }
    function render(message) {
      var max = Math.max.apply(null, values.concat([1]));
      lab.querySelector('[data-bars]').innerHTML = values.map(function (value, index) {
        var sorted = index >= values.length - pass;
        return '<div class="sort-bar-wrap"><i class="sort-bar' + (sorted ? ' sorted' : '') + '" style="height:' + Math.max(22, Math.round(value / max * 118)) + 'px"></i><b>' + value + '</b></div>';
      }).join('');
      lab.querySelector('[data-state]').textContent = '第 ' + pass + ' 趟后：' + values.join('，') + '；右侧 ' + pass + ' 个元素已归位。';
      lab.querySelector('[data-result]').textContent = message || '点击“执行下一趟”，从左向右比较相邻元素并把当前最大值送到末尾。';
      lab.querySelector('[data-next]').disabled = pass >= values.length - 1;
    }
    function reset() { values = readValues(); pass = 0; render('已载入新序列。冒泡排序每一趟至少确定一个末尾元素。'); }
    lab.querySelector('[data-reset]').addEventListener('click', reset);
    lab.querySelector('[data-next]').addEventListener('click', function () {
      var swapped = 0, end = values.length - pass - 1;
      for (var i = 0; i < end; i++) if (values[i] > values[i + 1]) { var temp = values[i]; values[i] = values[i + 1]; values[i + 1] = temp; swapped++; }
      pass++; render('本趟完成 ' + end + ' 次比较、' + swapped + ' 次交换；最大未归位元素已移动到有序区左边界。');
    });
    reset();
  }

  function mountArithmeticLab() {
    var chapter = document.getElementById('2');
    if (!chapter || document.querySelector('.arithmetic-lab')) return;
    var lab = document.createElement('section');
    lab.className = 'interactive-lab arithmetic-lab';
    lab.innerHTML = '<div class="lab-heading"><span>可交互可视化</span><h3>加法器与乘法器工作过程</h3><p>用 4 位无符号数观察全加器的逐位进位，以及“移位 + 累加”乘法器如何形成部分积。</p></div><div class="process-tabs" data-arithmetic-tabs><button type="button" data-mode="add" class="selected">4 位并行加法器</button><button type="button" data-mode="multiply">移位累加乘法器</button></div><div class="lab-controls"><label>A（0–15）<input data-a type="number" min="0" max="15" value="11"></label><label>B（0–15）<input data-b type="number" min="0" max="15" value="6"></label><button type="button" data-update>更新输入</button><button type="button" data-prev>上一步</button><button type="button" data-next>下一步</button></div><div class="adder-visual" data-adder></div><div class="multiplier-visual" data-multiplier hidden></div><p class="lab-result" data-result></p>';
    chapter.insertAdjacentElement('afterend', lab);
    var mode = 'add', mulStep = 0;
    function numberValue(selector) {
      var value = Number(lab.querySelector(selector).value);
      return Number.isFinite(value) ? Math.max(0, Math.min(15, Math.floor(value))) : 0;
    }
    function bits(value, width) { return value.toString(2).padStart(width, '0'); }
    function cell(value, extra) { return '<span class="bit-cell ' + (extra || '') + '">' + value + '</span>'; }
    function renderAdder(a, b) {
      var carry = [0], sum = [];
      for (var i = 0; i < 4; i++) {
        var total = ((a >> i) & 1) + ((b >> i) & 1) + carry[i];
        sum[i] = total & 1; carry[i + 1] = total >> 1;
      }
      var columns = [];
      for (var bit = 3; bit >= 0; bit--) {
        columns.push('<div class="full-adder-cell"><b>FA' + bit + '</b><small>A' + bit + ' + B' + bit + ' + C' + bit + '</small><div>' + cell((a >> bit) & 1, 'operand-a') + cell((b >> bit) & 1, 'operand-b') + cell(carry[bit], 'carry') + '</div><em>↓</em><div>' + cell(sum[bit], 'sum') + cell(carry[bit + 1], 'carry-out') + '</div><small>S' + bit + ' / C' + (bit + 1) + '</small></div>');
      }
      lab.querySelector('[data-adder]').innerHTML = '<div class="arithmetic-labels"><span>A = ' + bits(a, 4) + '₂ (' + a + ')</span><span>B = ' + bits(b, 4) + '₂ (' + b + ')</span><span>从低位向高位传递进位</span></div><div class="full-adder-grid">' + columns.join('<i class="carry-arrow">← C</i>') + '</div><div class="arithmetic-output">S = ' + carry[4] + bits(sum.reduce(function (total, bit, index) { return total + (bit << index); }, 0), 4) + '₂ = ' + (a + b) + '，最高位进位 C4 = ' + carry[4] + '</div>';
    }
    function renderMultiplier(a, b) {
      mulStep = Math.max(0, Math.min(mulStep, 3));
      var rows = [], accumulator = 0;
      for (var i = 0; i < 4; i++) {
        var bit = (b >> i) & 1;
        var partial = bit ? (a << i) : 0;
        accumulator += partial;
        var active = i === mulStep ? ' active' : (i < mulStep ? ' done' : '');
        rows.push('<article class="multiply-row' + active + '"><b>第 ' + (i + 1) + ' 拍</b><span>Q' + i + ' = ' + bit + '</span><span>' + (bit ? '累加 A << ' + i : '跳过（该位为 0）') + '</span><code>' + bits(partial, 8) + '</code><code>ACC = ' + bits(accumulator, 8) + '</code></article>');
      }
      var current = 0;
      for (var j = 0; j <= mulStep; j++) if ((b >> j) & 1) current += a << j;
      lab.querySelector('[data-multiplier]').innerHTML = '<div class="arithmetic-labels"><span>M（被乘数）= ' + bits(a, 4) + '₂</span><span>Q（乘数）= ' + bits(b, 4) + '₂</span><span>从 Q0 开始逐位判断</span></div><div class="multiplier-registers"><div><b>M</b><code>' + bits(a, 8) + '</code></div><div><b>Q</b><code>' + bits(b, 4) + '</code></div><div><b>ACC</b><code>' + bits(current, 8) + '</code></div></div><div class="multiply-steps">' + rows.join('') + '</div>';
    }
    function render() {
      var a = numberValue('[data-a]'), b = numberValue('[data-b]');
      lab.querySelector('[data-a]').value = a; lab.querySelector('[data-b]').value = b;
      renderAdder(a, b); renderMultiplier(a, b);
      lab.querySelector('[data-adder]').hidden = mode !== 'add';
      lab.querySelector('[data-multiplier]').hidden = mode !== 'multiply';
      lab.querySelector('[data-prev]').disabled = mode !== 'multiply' || mulStep === 0;
      lab.querySelector('[data-next]').disabled = mode !== 'multiply' || mulStep === 3;
      Array.prototype.forEach.call(lab.querySelectorAll('[data-mode]'), function (button) { button.classList.toggle('selected', button.dataset.mode === mode); });
      lab.querySelector('[data-result]').textContent = mode === 'add' ? '四个全加器可并行计算 S0–S3；但行波进位需从低位逐级传到高位。' : '当前累加器 ACC = ' + currentProduct(a, b, mulStep) + '；完成 4 拍后，A × B = ' + (a * b) + '。';
    }
    function currentProduct(a, b, step) {
      var result = 0;
      for (var i = 0; i <= step; i++) if ((b >> i) & 1) result += a << i;
      return result;
    }
    Array.prototype.forEach.call(lab.querySelectorAll('[data-mode]'), function (button) {
      button.addEventListener('click', function () { mode = button.dataset.mode; render(); });
    });
    lab.querySelector('[data-update]').addEventListener('click', function () { mulStep = 0; render(); });
    lab.querySelector('[data-prev]').addEventListener('click', function () { mulStep--; render(); });
    lab.querySelector('[data-next]').addEventListener('click', function () { mulStep++; render(); });
    render();
  }

  function mountCpuLab() {
    var chapter = document.getElementById('5-cpu');
    if (!chapter || document.querySelector('.cpu-lab')) return;
    var lab = document.createElement('section');
    lab.className = 'interactive-lab cpu-lab';
    lab.innerHTML = '<div class="lab-heading"><span>可交互可视化</span><h3>CPU 内部结构与指令通路</h3><p>按步骤播放一条指令：实线表示数据/地址通路，虚线表示控制信号；当前经过的模块与连线会高亮。</p></div><div class="lab-controls"><label>指令<select data-instruction><option value="load">LOAD R1, [0x100]</option><option value="add">ADD R3, R1, R2</option><option value="store">STORE R3, [0x104]</option></select></label><button type="button" data-prev>上一步</button><button type="button" data-next>下一步</button><button type="button" data-play>自动演示</button></div><pre class="assembly-line" data-assembly></pre><div class="machine-stage cpu-structure-stage"><svg viewBox="0 0 780 500" role="img" aria-label="CPU内部结构图，含PC、MAR、IR、控制单元、寄存器组、ALU、MDR与主存，以及数据流、地址流、控制信号流"><defs><marker id="cpu-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z"></path></marker></defs><text class="cpu-svg-title" x="390" y="32">CPU 内部结构图</text><rect class="cpu-frame" x="55" y="52" width="670" height="340" rx="22"></rect><text class="cpu-frame-label" x="390" y="82">CPU</text><g class="cpu-links" marker-end="url(#cpu-arrow)"><path data-cpu-link="pc-mar" class="address-flow" d="M225 147H285"></path><path data-cpu-link="mar-mem-read" class="address-flow" d="M345 180V420"></path><path data-cpu-link="mem-mdr" class="data-flow" d="M480 420V362H595"></path><path data-cpu-link="mdr-ir" class="data-flow" d="M595 302V180H535"></path><path data-cpu-link="ir-cu" class="control-flow" d="M475 180V210H395"></path><path data-cpu-link="cu-reg" class="control-flow" d="M450 255H500"></path><path data-cpu-link="cu-alu" class="control-flow" d="M395 302V328"></path><path data-cpu-link="reg-alu" class="data-flow" d="M560 310V338H500"></path><path data-cpu-link="alu-reg" class="data-flow" d="M500 365H560V310"></path><path data-cpu-link="alu-mar" class="address-flow" d="M335 350H285V180"></path><path data-cpu-link="mdr-reg" class="data-flow" d="M595 362V390H620V310"></path><path data-cpu-link="reg-mdr" class="data-flow" d="M650 310V390H595V362"></path><path data-cpu-link="mdr-mem-write" class="data-flow" d="M620 362V420H510"></path></g><g class="machine-node cpu-node pc-node" data-cpu-node="PC" transform="translate(105 112)"><rect width="120" height="68"></rect><text x="60" y="27">1. PC</text><text class="node-sub" x="60" y="47">程序计数器</text></g><g class="machine-node cpu-node mar-node" data-cpu-node="MAR" transform="translate(285 112)"><rect width="120" height="68"></rect><text x="60" y="27">MAR</text><text class="node-sub" x="60" y="47">地址寄存器</text></g><g class="machine-node cpu-node ir-node" data-cpu-node="IR" transform="translate(475 112)"><rect width="120" height="68"></rect><text x="60" y="27">2. IR</text><text class="node-sub" x="60" y="47">指令寄存器</text></g><g class="machine-node cpu-node cu-node" data-cpu-node="CU" transform="translate(280 210)"><rect width="170" height="92"></rect><text x="85" y="31">4. 控制单元（CU）</text><text class="node-sub" x="85" y="54">译码、产生控制信号</text><text class="node-sub" x="85" y="72">协调各部件工作</text></g><g class="machine-node cpu-node reg-node" data-cpu-node="REG" transform="translate(500 210)"><rect width="150" height="100"></rect><text x="75" y="27">5. 通用寄存器组</text><path class="register-lines" d="M20 40H80M20 56H80M20 72H80M20 88H80"></path><text class="node-sub" x="110" y="53">R0</text><text class="node-sub" x="110" y="70">R1 / R2</text><text class="node-sub" x="110" y="87">… Rn-1</text></g><g class="machine-node cpu-node alu-node" data-cpu-node="ALU" transform="translate(330 328)"><path class="alu-shape" d="M0 0H170L145 58H25Z"></path><text x="85" y="27">3. ALU</text><text class="node-sub" x="85" y="45">算术逻辑单元</text></g><g class="machine-node cpu-node mdr-node" data-cpu-node="MDR" transform="translate(560 328)"><rect width="110" height="68"></rect><text x="55" y="27">MDR</text><text class="node-sub" x="55" y="47">数据寄存器</text></g><g class="machine-node cpu-node mem-node" data-cpu-node="MEM" transform="translate(230 420)"><rect width="320" height="58"></rect><text x="160" y="25">主存储器</text><text class="node-sub" x="160" y="45">存放程序与数据</text></g><g class="flow-token" data-cpu-token transform="translate(165 105)"><circle r="10"></circle><text x="0" y="3">●</text></g><g class="cpu-legend"><path class="data-flow" d="M75 455H115"></path><text x="125" y="460">数据流</text><path class="control-flow" d="M75 477H115"></path><text x="125" y="482">控制信号流</text><path class="address-flow" d="M210 455H250"></path><text x="260" y="460">地址流</text></g></svg></div><div class="process-rail" data-rail></div><p class="lab-result" data-result></p>';
    chapter.insertAdjacentElement('afterend', lab);
    var flows = {
      load: { asm: 'LOAD R1, [0x100]    ; R1 ← M[0x100]', steps: [
        ['取指', 'PC → MAR → 主存 → MDR → IR', '用 PC 给出指令地址，主存读出指令并送入 IR；PC 更新到下一条。'],
        ['译码', 'IR → 控制器 → 寄存器堆', '控制器识别 LOAD，准备地址字段与目标寄存器 R1。'],
        ['执行', '地址字段 → ALU → MAR', 'ALU 计算有效地址 0x100，并写入 MAR。'],
        ['访存', 'MAR → 主存 → MDR', '主存读取地址 0x100 的数据，暂存到 MDR。'],
        ['写回', 'MDR → 寄存器堆（R1）', '数据写入 R1，指令完成。']
      ]},
      add: { asm: 'ADD R3, R1, R2       ; R3 ← R1 + R2', steps: [
        ['取指', 'PC → MAR → 主存 → MDR → IR', '读取 ADD 指令并送入 IR。'],
        ['译码', 'IR → 控制器 → 寄存器堆', '控制器读取源操作数 R1、R2 的编号。'],
        ['取数', '寄存器堆 → ALU 输入端', '寄存器堆并行读出 R1 和 R2。'],
        ['执行', 'ALU：R1 + R2', 'ALU 完成加法并更新状态标志位。'],
        ['写回', 'ALU → 寄存器堆（R3）', '运算结果写入目的寄存器 R3。']
      ]},
      store: { asm: 'STORE R3, [0x104]  ; M[0x104] ← R3', steps: [
        ['取指', 'PC → MAR → 主存 → MDR → IR', '取出 STORE 指令。'],
        ['译码', 'IR → 控制器 → 寄存器堆', '控制器识别源寄存器 R3 与目标地址字段。'],
        ['执行', '地址字段 → ALU → MAR', 'ALU 得到有效地址 0x104，送入 MAR。'],
        ['取数', '寄存器堆（R3） → MDR', '将 R3 的数据送入 MDR，准备写主存。'],
        ['写存', 'MDR → 主存[MAR]', '控制器发出写信号，数据写入主存。']
      ]}
    };
    var targets = { load: ['IR', 'CU', 'MAR', 'MDR', 'REG'], add: ['IR', 'CU', 'REG', 'ALU', 'REG'], store: ['IR', 'CU', 'MAR', 'MDR', 'MEM'] };
    var points = { PC:[165,105], MAR:[345,105], MEM:[390,410], MDR:[615,320], IR:[535,105], CU:[365,200], REG:[575,200], ALU:[415,320] };
    var activeLinks = {
      load: [['pc-mar', 'mar-mem-read', 'mem-mdr', 'mdr-ir'], ['ir-cu', 'cu-reg'], ['cu-alu', 'alu-mar'], ['mar-mem-read', 'mem-mdr'], ['mdr-reg']],
      add: [['pc-mar', 'mar-mem-read', 'mem-mdr', 'mdr-ir'], ['ir-cu', 'cu-reg'], ['reg-alu'], ['reg-alu', 'cu-alu'], ['alu-reg']],
      store: [['pc-mar', 'mar-mem-read', 'mem-mdr', 'mdr-ir'], ['ir-cu', 'cu-reg'], ['cu-alu', 'alu-mar'], ['reg-mdr'], ['mdr-mem-write']]
    };
    var step = 0, timer = null;
    function render() {
      var instruction = lab.querySelector('[data-instruction]').value;
      var flow = flows[instruction];
      step = Math.max(0, Math.min(step, flow.steps.length - 1));
      lab.querySelector('[data-assembly]').textContent = flow.asm;
      lab.querySelector('[data-rail]').innerHTML = flow.steps.map(function (item, i) {
        return '<article class="process-step ' + (i === step ? 'active' : '') + (i < step ? ' done' : '') + '"><span>' + (i + 1) + '</span><strong>' + item[0] + '</strong><b>' + item[1] + '</b></article>';
      }).join('');
      lab.querySelector('[data-result]').textContent = '第 ' + (step + 1) + ' 步：' + flow.steps[step][2];
      var activeNode = targets[instruction][step];
      Array.prototype.forEach.call(lab.querySelectorAll('[data-cpu-node]'), function (node) { node.classList.toggle('active', node.dataset.cpuNode === activeNode); });
      var links = activeLinks[instruction][step];
      Array.prototype.forEach.call(lab.querySelectorAll('[data-cpu-link]'), function (link) { link.classList.toggle('active', links.indexOf(link.dataset.cpuLink) > -1); });
      var point = points[activeNode];
      lab.querySelector('[data-cpu-token]').setAttribute('transform', 'translate(' + point[0] + ' ' + point[1] + ')');
    }
    lab.querySelector('[data-instruction]').addEventListener('change', function () { step = 0; render(); });
    lab.querySelector('[data-prev]').addEventListener('click', function () { step--; render(); });
    lab.querySelector('[data-next]').addEventListener('click', function () { step++; render(); });
    lab.querySelector('[data-play]').addEventListener('click', function () {
      if (timer) return;
      step = 0; render();
      timer = setInterval(function () {
        var flow = flows[lab.querySelector('[data-instruction]').value];
        if (step >= flow.steps.length - 1) { clearInterval(timer); timer = null; return; }
        step++; render();
      }, 900);
    });
    render();
  }

  function mountNetworkProcessLab() {
    var chapter = document.getElementById('1');
    if (!chapter || document.querySelector('.network-process-lab')) return;
    var lab = document.createElement('section');
    lab.className = 'interactive-lab network-process-lab';
    lab.innerHTML = '<div class="lab-heading"><span>可交互可视化</span><h3>网络协议过程演示</h3><p>选择主题后，逐步播放关键报文、设备与状态变化；适合梳理高频过程题。</p></div><div class="process-tabs" data-tabs></div><div class="network-stage"><svg viewBox="0 0 620 250" role="img" aria-label="终端、无线接入点、交换机、路由器与服务器之间的报文流动图"><defs><marker id="net-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z"></path></marker></defs><g class="machine-links" marker-end="url(#net-arrow)"><path d="M100 165H205"></path><path d="M275 165H355"></path><path d="M425 165H520"></path><path d="M70 130L225 65"></path><path d="M270 70L390 135"></path></g><g class="machine-node" data-net-node="CLIENT" transform="translate(25 135)"><rect width="80" height="60"></rect><text x="40" y="25">终端</text><text class="node-sub" x="40" y="43">Client / STA</text></g><g class="machine-node" data-net-node="AP" transform="translate(205 35)"><rect width="80" height="60"></rect><text x="40" y="25">AP</text><text class="node-sub" x="40" y="43">无线接入点</text></g><g class="machine-node" data-net-node="SWITCH" transform="translate(205 135)"><rect width="80" height="60"></rect><text x="40" y="25">交换机</text><text class="node-sub" x="40" y="43">VLAN / Trunk</text></g><g class="machine-node" data-net-node="ROUTER" transform="translate(355 135)"><rect width="80" height="60"></rect><text x="40" y="25">路由器</text><text class="node-sub" x="40" y="43">IP 网关</text></g><g class="machine-node" data-net-node="SERVER" transform="translate(515 135)"><rect width="80" height="60"></rect><text x="40" y="25">服务器</text><text class="node-sub" x="40" y="43">Server</text></g><g class="packet-token" data-net-token transform="translate(65 125)"><rect x="-35" y="-13" width="70" height="26"></rect><text data-packet-label text-anchor="middle" y="4">SYN</text></g></svg></div><div class="process-flow" data-flow></div><div class="lab-controls"><button type="button" data-prev>上一步</button><button type="button" data-next>下一步</button><button type="button" data-play>自动播放</button></div><p class="lab-result" data-result></p>';
    chapter.insertAdjacentElement('afterend', lab);
    var topologyIcons = {
      CLIENT: '<g class="topology-icon"><rect class="device-body" x="8" y="5" width="64" height="38" rx="4"></rect><rect class="device-screen" x="14" y="10" width="52" height="27" rx="2"></rect><path class="device-line" d="M40 43v8M24 52h32"></path><text class="topology-label" x="40" y="66">终端</text></g>',
      AP: '<g class="topology-icon"><rect class="device-body" x="20" y="36" width="40" height="14" rx="5"></rect><circle class="device-light" cx="40" cy="43" r="2"></circle><path class="device-line" d="M40 36V14M31 20q9-9 18 0M25 14q15-15 30 0"></path><text class="topology-label" x="40" y="66">无线 AP</text></g>',
      SWITCH: '<g class="topology-icon"><rect class="device-body" x="5" y="22" width="70" height="28" rx="6"></rect><path class="device-line" d="M13 31h8m5 0h8m5 0h8m5 0h8M13 40h8m5 0h8m5 0h8m5 0h8"></path><text class="topology-label" x="40" y="66">交换机</text></g>',
      ROUTER: '<g class="topology-icon"><circle class="device-body" cx="40" cy="34" r="24"></circle><path class="device-line" d="M25 29h25l-6-6m6 6-6 6M55 39H30l6 6m-6-6 6-6"></path><text class="topology-label" x="40" y="66">路由器</text></g>',
      SERVER: '<g class="topology-icon"><rect class="device-body" x="18" y="5" width="44" height="50" rx="5"></rect><path class="device-line" d="M24 19h32M24 33h32M24 47h32"></path><circle class="device-light" cx="28" cy="13" r="2"></circle><circle class="device-light" cx="28" cy="27" r="2"></circle><circle class="device-light" cx="28" cy="41" r="2"></circle><text class="topology-label" x="40" y="70">服务器</text></g>'
    };
    Array.prototype.forEach.call(lab.querySelectorAll('[data-net-node]'), function (node) {
      node.innerHTML = topologyIcons[node.dataset.netNode];
    });
    var scenarios = {
      VLAN: [
        ['终端 A', '发送未打标签的以太网帧，接入口将它归入 VLAN 10。'],
        ['交换机', '在 Trunk 链路上为帧加 802.1Q VLAN 10 标签。'],
        ['二层转发', '另一台交换机只在 VLAN 10 的端口范围内泛洪或转发。'],
        ['三层网关', '跨 VLAN 通信时，帧到达 VLAN 10 网关，再由路由器转发到目标 VLAN。']
      ],
      WLAN: [
        ['扫描', 'STA 扫描信道，发现 AP 的 Beacon（SSID、能力信息）。'],
        ['认证', 'STA 与 AP 完成认证；采用 WPA2/WPA3 时还会进行安全协商。'],
        ['关联', 'STA 发送 Association Request，AP 分配关联 ID。'],
        ['入网', 'STA 通过 DHCP 获取 IP、网关和 DNS，随后可正常传输数据。']
      ],
      DHCP: [
        ['Discover', '客户端无 IP，以广播发送 DHCPDISCOVER。'],
        ['Offer', '服务器提供可用地址、租约时间、网关和 DNS 配置。'],
        ['Request', '客户端广播 DHCPREQUEST，声明选择该服务器的地址。'],
        ['ACK', '服务器确认 DHCPACK；客户端配置地址并开始租约计时。']
      ],
      TCP: [
        ['SYN', '客户端发送 SYN，选择初始序号 seq=x，进入 SYN-SENT。'],
        ['SYN + ACK', '服务器确认 ack=x+1，同时发出自己的 SYN，进入 SYN-RCVD。'],
        ['ACK', '客户端确认 ack=y+1，双方进入 ESTABLISHED，可可靠传输字节流。'],
        ['挥手', '关闭时 FIN/ACK 往返，主动关闭方通常经历 TIME-WAIT。']
      ],
      UDP: [
        ['封装', '应用数据加上 8B UDP 首部：源/目的端口、长度、校验和。'],
        ['下交', 'UDP 直接交给 IP 层封装并路由，无连接建立阶段。'],
        ['交付', '接收端按目的端口交给应用；不保证到达、顺序或重传。'],
        ['适用', 'DNS、音视频、实时游戏等更重视低时延的业务常用 UDP。']
      ],
      ARP: [
        ['Request', '主机缓存未命中，以广播发送“谁有目标 IP？”的 ARP 请求。'],
        ['泛洪', '交换机在同一 VLAN 内泛洪该广播帧，不会跨越路由器。'],
        ['Reply', '目标主机以单播 ARP Reply 返回自己的 MAC 地址。'],
        ['缓存', '发送方写入 ARP 表，之后可按目标 MAC 封装以太网帧。']
      ],
      DNS: [
        ['递归查询', '客户端把域名查询交给本地 DNS 递归解析器。'],
        ['根提示', '解析器向根服务器询问顶级域服务器的位置。'],
        ['权威查询', '解析器继续向 TLD / 权威 DNS 查询目标记录。'],
        ['缓存返回', '解析器缓存 TTL 内的结果，并把 IP 地址返回客户端。']
      ],
      NAT: [
        ['出站转换', '私网主机发起连接，NAT 设备记录“私网 IP:端口 ↔ 公网 IP:端口”。'],
        ['公网转发', '报文源地址和源端口被改写后，转发到公网服务器。'],
        ['入站匹配', '服务器响应到达公网地址，NAT 用映射表匹配会话。'],
        ['还原交付', 'NAT 还原目的地址和端口，再转发回内网主机。']
      ],
      'TCP 拥塞控制': [
        ['慢开始', '拥塞窗口 cwnd 从小值开始，RTT 内近似指数增长。'],
        ['拥塞避免', '到达阈值 ssthresh 后，cwnd 改为线性增长。'],
        ['丢包反馈', '超时或三次重复 ACK 说明可能拥塞，需要降低发送速率。'],
        ['恢复', '快速重传 / 快速恢复后重新调整 cwnd 与 ssthresh。']
      ]
    };
    var route = {
      VLAN: ['CLIENT','SWITCH','AP','ROUTER'], WLAN: ['CLIENT','AP','AP','SERVER'], DHCP: ['CLIENT','SERVER','CLIENT','SERVER'], TCP: ['CLIENT','SERVER','CLIENT','SERVER'], UDP: ['CLIENT','SWITCH','ROUTER','SERVER'], ARP: ['CLIENT','SWITCH','SERVER','CLIENT'], DNS: ['CLIENT','SERVER','SERVER','CLIENT'], NAT: ['CLIENT','ROUTER','ROUTER','CLIENT'], 'TCP 拥塞控制': ['CLIENT','ROUTER','ROUTER','CLIENT']
    };
    var packetLabels = { VLAN:['帧','802.1Q','VLAN 10','跨 VLAN'], WLAN:['Probe','Auth','Assoc','DHCP'], DHCP:['Discover','Offer','Request','ACK'], TCP:['SYN','SYN+ACK','ACK','FIN'], UDP:['Data','UDP','IP','Deliver'], ARP:['Request','广播','Reply','MAC 表'], DNS:['Query','Root','A 记录','Answer'], NAT:['10.0.0.2','公网映射','匹配表','10.0.0.2'], 'TCP 拥塞控制':['cwnd=1','线性增','丢包','恢复'] };
    var topologies = {
      VLAN: { nodes: { CLIENT:[25,135], SWITCH:[180,135], AP:[330,135], ROUTER:[485,135] }, links: ['M105 165H180','M260 165H330','M410 165H485'] },
      WLAN: { nodes: { CLIENT:[25,135], AP:[190,35], SWITCH:[350,135], SERVER:[515,135] }, links: ['M70 135L230 95','M270 70L390 135','M430 165H515'] },
      DHCP: { nodes: { CLIENT:[25,135], SWITCH:[260,135], SERVER:[515,135] }, links: ['M105 165H260','M340 165H515'] },
      TCP: { nodes: { CLIENT:[25,135], ROUTER:[275,135], SERVER:[515,135] }, links: ['M105 165H275','M355 165H515'] },
      UDP: { nodes: { CLIENT:[25,135], SWITCH:[190,135], ROUTER:[350,135], SERVER:[515,135] }, links: ['M105 165H190','M270 165H350','M430 165H515'] },
      ARP: { nodes: { CLIENT:[25,135], SWITCH:[260,135], SERVER:[515,135] }, links: ['M105 165H260','M340 165H515'] },
      DNS: { nodes: { CLIENT:[25,135], ROUTER:[275,135], SERVER:[515,135] }, links: ['M105 165H275','M355 165H515'] },
      NAT: { nodes: { CLIENT:[25,135], ROUTER:[275,135], SERVER:[515,135] }, links: ['M105 165H275','M355 165H515'] },
      'TCP 拥塞控制': { nodes: { CLIENT:[25,135], ROUTER:[275,135], SERVER:[515,135] }, links: ['M105 165H275','M355 165H515'] }
    };
    var linkPaths = Array.prototype.slice.call(lab.querySelectorAll('.machine-links path'));
    function updateTopology() {
      var topology = topologies[name];
      Array.prototype.forEach.call(lab.querySelectorAll('[data-net-node]'), function (node) {
        var point = topology.nodes[node.dataset.netNode];
        node.style.display = point ? '' : 'none';
        if (point) node.setAttribute('transform', 'translate(' + point[0] + ' ' + point[1] + ')');
        node.innerHTML = name === 'VLAN' && node.dataset.netNode === 'AP' ? topologyIcons.SWITCH : topologyIcons[node.dataset.netNode];
      });
      linkPaths.forEach(function (path, i) {
        var d = topology.links[i];
        path.style.display = d ? '' : 'none';
        if (d) path.setAttribute('d', d);
      });
      return topology.nodes;
    }
    var name = 'TCP', step = 0, timer = null;
    function render() {
      var flow = scenarios[name];
      step = Math.max(0, Math.min(step, flow.length - 1));
      lab.querySelector('[data-tabs]').innerHTML = Object.keys(scenarios).map(function (key) { return '<button type="button" class="' + (key === name ? 'selected' : '') + '" data-name="' + key + '">' + key + '</button>'; }).join('');
      lab.querySelector('[data-flow]').innerHTML = flow.map(function (item, i) { return '<article class="process-step ' + (i === step ? 'active' : '') + (i < step ? ' done' : '') + '"><span>' + (i + 1) + '</span><strong>' + item[0] + '</strong><p>' + item[1] + '</p></article>'; }).join('');
      lab.querySelector('[data-result]').textContent = name + ' · 第 ' + (step + 1) + ' 步：' + flow[step][1];
      var positions = updateTopology();
      var nodeName = route[name][step], base = positions[nodeName], point = [base[0] + 40, base[1] - 10];
      Array.prototype.forEach.call(lab.querySelectorAll('[data-net-node]'), function (node) { node.classList.toggle('active', node.dataset.netNode === nodeName); });
      lab.querySelector('[data-net-token]').setAttribute('transform', 'translate(' + point[0] + ' ' + point[1] + ')');
      lab.querySelector('[data-packet-label]').textContent = packetLabels[name][step];
      Array.prototype.forEach.call(lab.querySelectorAll('[data-name]'), function (button) { button.addEventListener('click', function () { name = button.dataset.name; step = 0; render(); }); });
    }
    lab.querySelector('[data-prev]').addEventListener('click', function () { step--; render(); });
    lab.querySelector('[data-next]').addEventListener('click', function () { step++; render(); });
    lab.querySelector('[data-play]').addEventListener('click', function () {
      if (timer) return;
      step = 0; render();
      timer = setInterval(function () {
        if (step >= scenarios[name].length - 1) { clearInterval(timer); timer = null; return; }
        step++; render();
      }, 1000);
    });
    render();
  }

  function mountSchedulerLab() {
    var chapter = document.getElementById('2');
    if (!chapter || document.querySelector('.scheduler-lab')) return;
    var lab = document.createElement('section');
    lab.className = 'interactive-lab scheduler-lab';
    lab.innerHTML = '<div class="lab-heading"><span>可交互可视化</span><h3>FCFS 调度甘特图</h3><p>调整三个进程的到达时间与运行时间，观察先来先服务的执行顺序和完成时刻。</p></div><div class="lab-controls"><label>P1 到达/运行<input data-p1 value="0,3"></label><label>P2 到达/运行<input data-p2 value="1,5"></label><label>P3 到达/运行<input data-p3 value="2,2"></label><button type="button" data-run>生成甘特图</button></div><div class="gantt" data-gantt></div><p class="lab-result" data-result></p>';
    chapter.insertAdjacentElement('afterend', lab);
    function parse(value, name) {
      var pair = value.split(',').map(Number);
      return { name: name, arrival: Math.max(0, pair[0] || 0), burst: Math.max(1, pair[1] || 1) };
    }
    function render() {
      var jobs = ['P1', 'P2', 'P3'].map(function (name) { return parse(lab.querySelector('[data-' + name.toLowerCase() + ']').value, name); });
      jobs.sort(function (a, b) { return a.arrival - b.arrival || a.name.localeCompare(b.name); });
      var time = 0;
      jobs.forEach(function (job) { job.start = Math.max(time, job.arrival); job.end = job.start + job.burst; time = job.end; });
      lab.querySelector('[data-gantt]').innerHTML = jobs.map(function (job) {
        return '<div class="gantt-item" style="flex:' + job.burst + '"><b>' + job.name + '</b><span>' + job.start + ' → ' + job.end + '</span></div>';
      }).join('');
      lab.querySelector('[data-result]').textContent = '执行顺序：' + jobs.map(function (j) { return j.name; }).join(' → ') + '；最后完成时刻：' + time + '。';
    }
    lab.querySelector('[data-run]').addEventListener('click', render);
    render();
  }

  function mountPageReplacementLab() {
    var chapter = document.getElementById('3');
    if (!chapter || document.querySelector('.page-replacement-lab')) return;
    var lab = document.createElement('section');
    lab.className = 'interactive-lab page-replacement-lab';
    lab.innerHTML = '<div class="lab-heading"><span>可交互可视化</span><h3>LRU 页面置换过程</h3><p>按访问串逐步推进，观察命中、缺页和最近最久未使用页被换出的瞬间。</p></div><div class="lab-controls"><label>访问串（逗号分隔）<input data-refs value="7,0,1,2,0,3,0,4"></label><label>页框数<select data-frames><option>2</option><option selected>3</option><option>4</option></select></label><button type="button" data-reset>重新开始</button><button type="button" data-next>访问下一页</button></div><div class="reference-strip" data-strip></div><div class="page-frames" data-page-frames></div><p class="lab-result" data-result></p>';
    chapter.insertAdjacentElement('afterend', lab);
    var refs = [], frames = [], usage = [], step = -1, faults = 0;
    function load() {
      refs = lab.querySelector('[data-refs]').value.split(',').map(function (item) { return Number(item.trim()); }).filter(function (n) { return Number.isInteger(n) && n >= 0; }).slice(0, 12);
      if (!refs.length) refs = [7, 0, 1, 2, 0, 3, 0, 4];
      frames = []; usage = []; step = -1; faults = 0; render('已重置。LRU 在缺页且页框满时，淘汰最久没有被访问的页面。');
    }
    function render(message) {
      lab.querySelector('[data-strip]').innerHTML = refs.map(function (ref, index) { return '<span class="reference-cell' + (index === step ? ' active' : '') + (index < step ? ' done' : '') + '">' + ref + '</span>'; }).join('');
      var count = Number(lab.querySelector('[data-frames]').value);
      lab.querySelector('[data-page-frames]').innerHTML = Array.from({ length: count }, function (_, index) { var value = frames[index]; return '<div class="page-frame' + (value === refs[step] ? ' active' : '') + '"><b>页框 ' + (index + 1) + '</b><span>' + (value === undefined ? '—' : value) + '</span></div>'; }).join('');
      lab.querySelector('[data-result]').textContent = message + ' 当前缺页次数：' + faults + '。';
      lab.querySelector('[data-next]').disabled = step >= refs.length - 1;
    }
    lab.querySelector('[data-reset]').addEventListener('click', load);
    lab.querySelector('[data-frames]').addEventListener('change', load);
    lab.querySelector('[data-next]').addEventListener('click', function () {
      step++; var page = refs[step], index = frames.indexOf(page), count = Number(lab.querySelector('[data-frames]').value), message;
      if (index >= 0) { usage[index] = step; message = '访问页 ' + page + '：命中，更新其最近使用时刻。'; }
      else {
        faults++;
        if (frames.length < count) { frames.push(page); usage.push(step); message = '访问页 ' + page + '：缺页，装入空闲页框。'; }
        else { var oldest = usage.indexOf(Math.min.apply(null, usage)), removed = frames[oldest]; frames[oldest] = page; usage[oldest] = step; message = '访问页 ' + page + '：缺页，淘汰最久未使用页 ' + removed + '。'; }
      }
      render(message);
    });
    load();
  }

  function boot() {
    var title = document.title;
    if (title.indexOf('计算机组成原理') > -1) { mountCacheLab(); mountArithmeticLab(); mountCpuLab(); }
    if (title.indexOf('计算机网络') > -1) { mountNetworkLab(); mountNetworkProcessLab(); }
    if (title.indexOf('数据结构') > -1) { mountStackLab(); mountSortLab(); }
    if (title.indexOf('操作系统') > -1) { mountSchedulerLab(); mountPageReplacementLab(); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
