#!/bin/bash
# 408 四科 GPT Image 2 批量配图生成脚本
# 使用 medium quality + 1k resolution

set -e

WORKSPACE="/Users/ahs/Documents/kimi/workspace/考研冲刺君/website/images"
QUALITY="medium"
RESOLUTION="1k"

generate_image() {
    local filename="$1"
    local prompt="$2"
    local aspect="${3:-4:3}"
    
    echo "[生成] $filename..."
    local result
    result=$(higgsfield generate create gpt_image_2 \
        --prompt "$prompt" \
        --quality "$QUALITY" \
        --resolution "$RESOLUTION" \
        --aspect_ratio "$aspect" \
        --wait --wait-timeout 5m 2>&1)
    
    # 提取URL
    local url=$(echo "$result" | grep -o 'https://[^[:space:]]*\.png' | head -1)
    
    if [ -n "$url" ]; then
        curl -sL -o "$WORKSPACE/$filename" "$url"
        echo "[完成] $filename ($(ls -lh "$WORKSPACE/$filename" | awk '{print $5}'))"
    else
        echo "[失败] $filename - $result"
    fi
}

# ========== 数据结构 (DS) ==========
echo "=== 数据结构配图 ==="

generate_image "ds_ch1_intro.png" \
    "Educational diagram showing abstract data types (ADT) concept: a box labeled 'ADT' with arrows pointing to concrete data structures (array, linked list, stack, queue, tree, graph). Clean white background, Chinese textbook style, computer science education illustration, labeled in Chinese"

generate_image "ds_ch2_linked_list.png" \
    "Realistic educational diagram of a singly linked list data structure: nodes with data fields and pointer fields connected by arrows, showing head node, middle nodes, and tail pointing to NULL. Clean white background, Chinese computer science textbook style, labeled in Chinese"

generate_image "ds_ch3_stack_queue.png" \
    "Educational comparison diagram showing Stack (LIFO) on left with push/pop arrows, and Queue (FIFO) on right with enqueue/dequeue arrows. Both shown as vertical containers with elements. Clean white background, Chinese textbook style, computer science education, labeled in Chinese"

generate_image "ds_ch4_tree.png" \
    "Realistic educational diagram of a binary tree with root, left child, right child, leaf nodes. Show preorder/inorder/postorder traversal paths with colored arrows. Node values are numbers. Clean white background, Chinese computer science textbook style, labeled in Chinese"

generate_image "ds_ch5_graph.png" \
    "Educational diagram showing graph data structure: vertices as circles with letters A-F, edges as lines connecting them. Show both directed edges (with arrows) and undirected edges. Adjacency matrix table on the side. Clean white background, Chinese textbook style, labeled in Chinese"

generate_image "ds_ch6_search.png" \
    "Realistic educational diagram comparing search algorithms: left side shows binary search on a sorted array with mid-pointer comparisons, right side shows hash table with hash function mapping keys to buckets. Clean white background, Chinese computer science textbook style, labeled in Chinese"

generate_image "ds_ch7_sort.png" \
    "Educational diagram showing sorting algorithm visualization: an array of numbered bars in different heights being sorted, with arrows showing swaps and comparisons. Show bubble sort passes with colored highlights. Clean white background, Chinese textbook style, labeled in Chinese"

# ========== 计组 (CO) ==========
echo "=== 计组配图 ==="

generate_image "co_ch1_overview.png" \
    "Educational diagram of von Neumann computer architecture: CPU (ALU + Control Unit), Memory, Input/Output devices connected by system bus (data bus, address bus, control bus). Clean white background, Chinese computer science textbook style, labeled in Chinese"

generate_image "co_ch2_data_representation.png" \
    "Realistic educational diagram showing number systems: binary, octal, decimal, hexadecimal conversion table. Show IEEE 754 floating point format with sign bit, exponent, mantissa fields. Clean white background, Chinese computer science textbook style, labeled in Chinese"

generate_image "co_ch3_memory.png" \
    "Educational diagram of computer memory hierarchy pyramid: registers at top, then cache (L1/L2/L3), main memory (DRAM), then SSD/HDD at bottom. Show access time and capacity labels. Clean white background, Chinese textbook style, labeled in Chinese"

generate_image "co_ch4_instruction.png" \
    "Realistic educational diagram showing CPU instruction format: opcode field and address field. Show instruction cycle steps (fetch, decode, execute, memory access, write back) as a flowchart. Clean white background, Chinese computer science textbook style, labeled in Chinese"

generate_image "co_ch5_cpu.png" \
    "Educational diagram of CPU internal structure: Program Counter, Instruction Register, ALU, Control Unit, Registers. Show data flow between components with arrows. Clean white background, Chinese computer science textbook style, labeled in Chinese"

generate_image "co_ch6_bus.png" \
    "Realistic educational diagram of computer bus system: system bus connecting CPU, memory, and I/O devices. Show three types: data bus (bidirectional), address bus (unidirectional), control bus. Clean white background, Chinese textbook style, labeled in Chinese"

# ========== OS ==========
echo "=== OS配图 ==="

generate_image "os_ch1_overview.png" \
    "Educational diagram showing operating system position: OS as a layer between hardware (CPU, memory, disk, I/O) and applications (browser, editor, game). Show system calls as the interface. Clean white background, Chinese computer science textbook style, labeled in Chinese"

generate_image "os_ch2_process.png" \
    "Realistic educational diagram of process states: New, Ready, Running, Waiting, Terminated. Show transitions between states with arrows and labels (dispatch, interrupt, I/O wait, exit). PCB box on the side. Clean white background, Chinese textbook style, labeled in Chinese"

generate_image "os_ch3_memory.png" \
    "Educational diagram of virtual memory system: logical address space divided into pages, physical memory divided into frames, page table mapping between them. Show page fault handling flow. Clean white background, Chinese computer science textbook style, labeled in Chinese"

generate_image "os_ch4_file.png" \
    "Realistic educational diagram of file system structure: directory tree with root, subdirectories, and files. Show file control block (FCB) contents: filename, size, permissions, pointers. Inode structure on the side. Clean white background, Chinese textbook style, labeled in Chinese"

generate_image "os_ch5_io.png" \
    "Educational diagram of I/O system architecture: I/O devices, device controllers, device drivers, and OS I/O subsystem layers. Show interrupt-driven I/O and DMA transfer paths. Clean white background, Chinese computer science textbook style, labeled in Chinese"

# ========== 计网 (CN) ==========
echo "=== 计网配图 ==="

generate_image "cn_ch1_architecture.png" \
    "Realistic educational diagram comparing OSI 7-layer model and TCP/IP 4-layer model side by side. OSI layers: Physical, Data Link, Network, Transport, Session, Presentation, Application. TCP/IP: Network Interface, Internet, Transport, Application. Arrows showing mapping between layers. Clean white background, Chinese textbook style, labeled in Chinese"

generate_image "cn_ch2_physical.png" \
    "Educational diagram of physical layer concepts: signal encoding (NRZ, Manchester), transmission media (twisted pair, coaxial, fiber optic, wireless), modulation (AM, FM, PM). Show waveform diagrams. Clean white background, Chinese textbook style, labeled in Chinese"

generate_image "cn_ch3_datalink.png" \
    "Realistic educational diagram of data link layer: frames with header (source MAC, dest MAC, type) and trailer (FCS). Show CSMA/CD protocol: stations sensing channel, collision detection, binary exponential backoff. Clean white background, Chinese textbook style, labeled in Chinese"

generate_image "cn_ch4_network.png" \
    "Educational diagram of network layer: IP packet structure (header with source/dest IP, TTL, protocol, checksum). Show routing table with destination, next hop, interface. Router forwarding packets between networks. Clean white background, Chinese textbook style, labeled in Chinese"

generate_image "cn_ch5_transport.png" \
    "Realistic educational diagram of TCP connection: three-way handshake (SYN, SYN-ACK, ACK) and four-way termination (FIN, ACK, FIN, ACK). Show TCP segment header with sequence number, acknowledgment number, window size. Clean white background, Chinese textbook style, labeled in Chinese"

generate_image "cn_ch6_application.png" \
    "Educational diagram of application layer protocols: HTTP request/response between client and server, DNS hierarchical resolution (root, TLD, authoritative), SMTP email flow. Client-server model with sockets. Clean white background, Chinese textbook style, labeled in Chinese"

echo "=== 全部生成完成 ==="
ls -lh "$WORKSPACE"/ds_ch*.png "$WORKSPACE"/co_ch*.png "$WORKSPACE"/os_ch*.png "$WORKSPACE"/cn_ch*.png 2>/dev/null || true
