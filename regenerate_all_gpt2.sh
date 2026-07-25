#!/bin/bash
# 批量用 GPT Image 2 替换 matplotlib 图片
# 使用 medium quality + 1k resolution

set -e
DIR="/Users/ahs/Documents/kimi/workspace/考研冲刺君/website/images"

gen() {
    local file="$1"
    local prompt="$2"
    echo "[生成] $file..."
    local url
    url=$(higgsfield generate create gpt_image_2 \
        --prompt "$prompt" \
        --quality medium --resolution 1k --aspect_ratio 4:3 \
        --wait --wait-timeout 5m 2>&1 | grep -o 'https://[^[:space:]]*\.png' | head -1)
    if [ -n "$url" ]; then
        curl -sL -o "$DIR/$file" "$url"
        echo "[完成] $file"
    else
        echo "[失败] $file"
    fi
}

# 数学一 (8张)
gen "math_tree.png" "Educational mind map diagram of calculus, linear algebra, and probability theory for Chinese graduate entrance exam (考研数学一). Three main branches: 高等数学 (limits, derivatives, integrals, series, differential equations), 线性代数 (determinants, matrices, eigenvalues, quadratic forms), 概率论与数理统计 (random variables, distributions, estimation, hypothesis testing). Clean white background, textbook style, Chinese labels, professional educational illustration"

gen "math_discontinuity_types.png" "Educational diagram showing three types of discontinuity points in calculus: removable discontinuity (hole), jump discontinuity (step), and infinite discontinuity (vertical asymptote). Number line with function curves, labeled in Chinese for graduate exam math. Clean white background, textbook style"

gen "math_derivative_geometric.png" "Educational diagram showing geometric meaning of derivative: curve y=x^2 with tangent line at point (1,1), secant lines approaching tangent. Labels: 切线斜率=导数, 割线→切线. Clean white background, Chinese graduate exam math style"

gen "math_extrema_concavity.png" "Educational diagram showing function extrema and concavity: curve with local maximum and minimum points marked, separate curves showing concave up (凹) and concave down (凸). Chinese labels, clean white background, textbook style"

gen "math_mvt_diagram.png" "Educational diagram of Lagrange Mean Value Theorem: continuous curve between two points with dashed secant line, showing a point where tangent is parallel to secant. Formula: f'(ξ)=(f(b)-f(a))/(b-a). Chinese labels, clean white background, textbook style"

gen "math_integral_area.png" "Educational diagram showing three applications of definite integral: (1) area under curve, (2) solid of revolution around x-axis, (3) cylindrical shell method around y-axis. Three panels, Chinese labels, clean white background, textbook style"

gen "math_chain_rule.png" "Educational diagram of multivariable chain rule: tree diagram showing z depends on u,v, which depend on x,y. Partial derivative arrows with multiplication and addition. Chinese labels, clean white background, textbook style"

gen "math_green_theorem.png" "Educational diagram of Green's Theorem: closed region D with counterclockwise boundary L, showing relationship between line integral and double integral. Formula: ∮_L Pdx+Qdy = ∬_D (∂Q/∂x - ∂P/∂y)dσ. Chinese labels, clean white background, textbook style"

gen "math_matrix_eigenvalue.png" "Educational diagram of matrix eigenvalue decomposition: vector x transformed by matrix A, showing direction unchanged but scaled by λ. Equation Ax=λx with arrows. Chinese labels, clean white background, textbook style"

# 英语一 (4张)
gen "english_pie.png" "Educational pie chart showing English test question type distribution: 阅读理解A 40分, 写作 30分, 新题型 10分, 完形填空 10分, 翻译 10分. Chinese labels, clean white background, textbook style"

gen "english_question_types.png" "Educational bar chart showing reading comprehension question types: 细节理解 9题, 推理判断 5题, 主旨大意 2题, 词义猜测 2题, 作者态度 2题. Chinese labels, clean white background, textbook style"

gen "english_reading_flow.png" "Educational flowchart showing reading comprehension problem-solving steps: 浏览题干(30s) → 划出关键词 → 回原文定位 → 细比对 → 选答案. Horizontal flow with arrows, total time 15-18 min. Chinese labels, clean white background, textbook style"

gen "english_writing_structure.png" "Educational diagram showing English essay structure: three sections - Paragraph 1 (describe picture/chart), Paragraph 2 (analysis and argument), Paragraph 3 (conclusion and suggestion). Chinese labels showing sentence counts and key elements, clean white background, textbook style"

# 数据结构 (4张)
gen "ds_tree_traversal.png" "Educational diagram showing binary tree traversal methods: preorder (root-left-right), inorder (left-root-right), postorder (left-right-root). Binary tree with nodes numbered 1-7, three traversal sequences shown with colored paths. Chinese labels, clean white background, textbook style"

gen "ds_sort_complexity.png" "Educational comparison chart of sorting algorithms: bubble sort, selection sort, insertion sort, quick sort, merge sort, heap sort. Showing time complexity (best/average/worst) and space complexity. Bar chart style, Chinese labels, clean white background, textbook style"

gen "ds_huffman.png" "Educational diagram showing Huffman tree construction: frequency table, merging lowest frequency nodes step by step, final tree with weighted path length. Chinese labels, clean white background, textbook style"

gen "ds_bst.png" "Educational diagram of binary search tree: root 50, left subtree 30/20/40, right subtree 70/60/80. Showing BST property: left < root < right. Search path for 40 highlighted. Chinese labels, clean white background, textbook style"

gen "ds_btree.png" "Educational diagram of B+ tree structure: root node with key, internal nodes, leaf nodes with data, leaf nodes linked in order. Chinese labels showing B+ tree properties, clean white background, textbook style"

gen "ds_graph.png" "Educational diagram comparing DFS and BFS: same 5-node graph, left side DFS with stack (deep first), right side BFS with queue (level by level). Traversal order shown with numbers. Chinese labels, clean white background, textbook style"

gen "ds_linked_list_ops.png" "Educational diagram of linked list operations: top shows singly linked list (head→A→B→C→NULL), bottom left shows insertion (insert X after A), bottom right shows deletion (remove B). Node structure with data and pointer fields. Chinese labels, clean white background, textbook style"

gen "ds_stack_queue.png" "Educational comparison of stack and queue: left stack (LIFO) with push/pop arrows, vertical container; right queue (FIFO) with enqueue/dequeue arrows, horizontal container. Chinese labels, clean white background, textbook style"

# 计组 (6张)
gen "co_storage_hierarchy.png" "Educational pyramid diagram of memory hierarchy: registers (fastest, smallest) at top, L1/L2/L3 cache, main memory (DRAM), SSD/HDD (slowest, largest) at bottom. Access time and capacity labels. Chinese labels, clean white background, textbook style"

gen "co_cache_mapping.png" "Educational diagram comparing cache mapping: direct mapped (1-way), 2-way set associative, fully associative. Each showing cache lines and memory blocks. Chinese labels, clean white background, textbook style"

gen "co_virtual_memory.png" "Educational diagram of virtual to physical address translation: CPU sends virtual address, page table/TLB lookup, physical address to main memory. TLB hit and miss paths shown. Chinese labels, clean white background, textbook style"

gen "co_floating_point.png" "Educational diagram of IEEE 754 single precision format: 1 bit sign, 8 bits exponent, 23 bits mantissa. Example showing -5.0 in binary. Three fields colored differently. Chinese labels, clean white background, textbook style"

gen "co_instruction_cycle.png" "Educational flowchart of instruction cycle: fetch → decode → execute → memory access → write back. Each step with CPU operations. Chinese labels, clean white background, textbook style"

gen "co_cpu_pipeline.png" "Educational diagram of 5-stage CPU pipeline: IF (fetch), ID (decode), EX (execute), MEM (memory), WB (write back). Pipeline timing diagram showing instruction flow through stages. Chinese labels, clean white background, textbook style"

# OS (12张)
gen "os_process_states.png" "Educational diagram of process state transitions: New → Ready → Running → Waiting → Terminated. Arrows labeled with dispatch, interrupt, I/O request, I/O completion, exit. PCB box on side. Chinese labels, clean white background, textbook style"

gen "os_page_replacement.png" "Educational comparison chart of page replacement algorithms: FIFO, OPT, LRU, CLOCK. Showing page reference string and frame contents step by step. Page fault counts compared. Chinese labels, clean white background, textbook style"

gen "os_deadlock_conditions.png" "Educational diagram of four deadlock conditions: mutual exclusion, hold and wait, no preemption, circular wait. Four interconnected boxes with explanations. Chinese labels, clean white background, textbook style"

gen "os_disk_schedule.png" "Educational diagram comparing disk scheduling algorithms: FCFS, SSTF, SCAN, C-SCAN. Disk head movement paths shown on cylinder number line. Chinese labels, clean white background, textbook style"

gen "os_file_system.png" "Educational diagram of file system structure: directory tree (root, subdirectories, files), file control block contents, inode structure. Chinese labels, clean white background, textbook style"

gen "os_io_layers.png" "Educational diagram of I/O system layers: user space, system call interface, device-independent layer, device drivers, interrupt handlers, hardware. Chinese labels, clean white background, textbook style"

gen "os_kernel_user_mode.png" "Educational diagram showing kernel mode vs user mode: two privilege levels with system call as bridge. PSW register showing mode bit. Chinese labels, clean white background, textbook style"

gen "os_process_sync.png" "Educational diagram of process synchronization: critical section problem, Peterson's solution, semaphore operations (wait/signal). Producer-consumer example. Chinese labels, clean white background, textbook style"

gen "os_scheduling_comparison.png" "Educational bar chart comparing CPU scheduling algorithms: FCFS, SJF, RR, Priority. Average waiting time and turnaround time. Chinese labels, clean white background, textbook style"

gen "os_system_call.png" "Educational flowchart of system call execution: user program → trap instruction → kernel mode → system call handler → return to user mode. Chinese labels, clean white background, textbook style"

gen "os_memory_hierarchy.png" "Educational pyramid of memory hierarchy: registers, cache, main memory, disk. Showing speed vs capacity tradeoff. Chinese labels, clean white background, textbook style"

gen "os_virtual_memory.png" "Educational diagram of virtual memory: logical address space with pages, physical memory with frames, page table mapping. Page fault handling flow. Chinese labels, clean white background, textbook style"

# 计网 (4张)
gen "cn_osi_tcpip.png" "Educational side-by-side comparison of OSI 7-layer and TCP/IP 4-layer models. OSI: Physical, Data Link, Network, Transport, Session, Presentation, Application. TCP/IP: Network Interface, Internet, Transport, Application. Mapping arrows between layers. Chinese labels, clean white background, textbook style"

gen "cn_tcp_congestion.png" "Educational diagram of TCP congestion control: slow start (exponential growth), congestion avoidance (linear), timeout (reset to 1), fast recovery after 3 duplicate ACKs. Congestion window vs time graph. Chinese labels, clean white background, textbook style"

gen "cn_tcp_handshake.png" "Educational diagram of TCP three-way handshake and four-way termination: SYN, SYN-ACK, ACK for connection; FIN, ACK, FIN, ACK for termination. Sequence numbers shown. Chinese labels, clean white background, textbook style"

gen "cn_routing_protocols.png" "Educational comparison table of routing protocols: RIP (distance vector), OSPF (link state), BGP (path vector). Showing metrics, convergence, scalability. Chinese labels, clean white background, textbook style"

# 主页 (1张)
gen "timeline.png" "Educational timeline diagram showing three phases of graduate exam preparation: 基础夯实期 (3-6月, foundation), 强化突破期 (7-9月, strengthening), 冲刺模考期 (10-12月, sprint). Horizontal timeline with milestones and subjects. Chinese labels, clean white background, textbook style"

echo "=== All done ==="
