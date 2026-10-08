// Add verified publication years, exact BibTeX text, and local PDF paths here.
// Store PDFs in this site's repository (e.g. "papers/tollhelper.pdf") so the
// download attribute works reliably. Acceptance dates are not publication years.
const publicationResources = {
  'decentralized-digital-twins': {"year": 2026, "bib": "@INPROCEEDINGS{11659325,\n  author={Zhou, Mengbing and Zhao, Zhiming},\n  booktitle={2026 22nd International Conference on Distributed Computing in Smart Systems and the Internet of Things (DCOSS-IoT)},\n  title={(POSTER) Multi-Agent Framework for Decentralized Digital Twins},\n  year={2026},\n  volume={},\n  number={},\n  pages={331-333},\n  keywords={Internet of Things;Schedules;Timing;Scheduling;Digital twins;Printing;Digital Twin;Multi-Agent Systems;Decentralized Architecture;Function-as-a-Service;Task Offloading},\n  doi={10.1109/DCOSS-IoT69657.2026.00055}}", "pdf": "pdf/POSTER_Multi-Agent_Framework_for_Decentralized_Digital_Twins.pdf"},
  'multi-agent-faas': {"year": 2026, "bib": "@INPROCEEDINGS{11651941,\n  author={Lei, Yitao and Zhou, Mengbing and Daniëlse, Paul and Zhao, Zhiming},\n  booktitle={2026 IEEE International Parallel and Distributed Processing Symposium Workshops (IPDPSW)},\n  title={Multi-Agent Based Time Critical FaaS Scheduling in Edge-Cloud Continuum},\n  year={2026},\n  volume={},\n  number={},\n  pages={498-505},\n  keywords={Architecture;Computer architecture;Schedules;Scheduling;Tail;Timing;Clouds;Quality of service;Printing;Modeling;Serverless Computing;Edge–Cloud Continuum;Multi-Agent Scheduling;Architecture Evolution},\n  doi={10.1109/IPDPSW71298.2026.00085}}", "pdf": "pdf/Multi-Agent_Based_Time_Critical_FaaS_Scheduling_in_Edge-Cloud_Continuum.pdf"},
  'tollhelper': {"year": 2024, "bib": "@INPROCEEDINGS{10885367,\n  author={Zhou, Mengbing and Zhao, Bocong and Xu, Minxian and Dai, Hao and Wang, Yang},\n  booktitle={2024 IEEE International Symposium on Parallel and Distributed Processing with Applications (ISPA)}, \n  title={TollHelper: A Safe and Efficient Traffic Control Approach on Toll Plaza via Constrained Load Balancing}, \n  year={2024},\n  volume={},\n  number={},\n  pages={378-385},\n  keywords={Heuristic algorithms;Transportation;Traffic control;Load management;Dynamic scheduling;Hazards;Resource management;Surges;Traffic congestion;Standards;toll plaza;heterogeneous efficiency;load balancing;batch scheduling;safety},\n  doi={10.1109/ISPA63168.2024.00055}}", "pdf": "pdf/TollHelper_A_Safe_and_Efficient_Traffic_Control_Approach_on_Toll_Plaza_via_Constrained_Load_Balancing.pdf"},
  'spark-mpi-survey': {"year": 2025, "bib": "@ARTICLE{10970102,\n  author={Zhou, Mengbing and Li, Qiuyan and Cai, Mingyuan and Xu, Chengzhong and Wang, Yang},\n  journal={IEEE Transactions on Services Computing}, \n  title={Towards Hybrid Architectures for Big Data Analytics: Insights From Spark-MPI Integration}, \n  year={2025},\n  volume={18},\n  number={3},\n  pages={1852-1868},\n  keywords={Big Data;Sparks;Computer architecture;Surveys;Fault tolerant systems;Fault tolerance;Computational efficiency;Training;Parallel processing;Scalability;Spark;MPI;big data;high-performance computing;dual-intensive application;integration technology},\n  doi={10.1109/TSC.2025.3562342}}", "pdf": "pdf/Towards_Hybrid_Architectures_for_Big_Data_Analytics_Insights_From_Spark-MPI_Integration.pdf"},
  'batch-ordered-job-store': {"year": 2025, "bib": "@ARTICLE{11145330,\n  author={Zhou, Mengbing and Wang, Yang and Zhao, Bocong and Xu, Chengzhong},\n  journal={IEEE Transactions on Computers}, \n  title={Load Balancing Scheduling for Batch-Ordered Job-Store: Online vs. Offline}, \n  year={2025},\n  volume={74},\n  number={11},\n  pages={3778-3791},\n  keywords={Scheduling;Optimal scheduling;Heuristic algorithms;Load management;Dynamic scheduling;Processor scheduling;Load modeling;Job shop scheduling;Training;Resource management;Job-store;round-robin;load balancing;competitive ratio;circular sequence alignment.},\n  doi={10.1109/TC.2025.3603725}}", "pdf": "pdf/Load_Balancing_Scheduling_for_Batch-Ordered_Job-Store_Online_vs._Offline.pdf"},
  'spark-mpi-platform': {"year": 2025, "bib": "@Article{A10,\ntitle = {基于 Spark 与 MPI 集成的数据分析与处理平台},\njournal = {集成技术},\nvolume = {14},\nnumber = {4},\npages = {106-119},\nyear = {2025},\nissn = {2095-3135},\ndoi = {10.12146/j.issn.2095-3135.20241203002},\nurl = {https://jcjs.siat.ac.cn/cn/article/doi/10.12146/j.issn.2095-3135.20241203002},\nauthor = {周梦兵 and 李秋彦 and 吴欧 and 王洋}\n}", "pdf": "pdf/基于 Spark 与 MPI 集成的数据分析与处理平台.pdf"},
  'cloudhive': {"year": 2025, "bib": "@article{https://doi.org/10.1002/cpe.70238,\n  author = {Kent, Kenneth B. and Zhou, Mengbing and Adeyemo, Gabriel and Wang, Yang},\n  title = {Cloudhive: A Cloud-Based Framework for Smart Grid Co-Simulation, Data, and Communication},\n  journal = {Concurrency and Computation: Practice and Experience},\n  volume = {37},\n  number = {21-22},\n  pages = {e70238},\n  keywords = {big data, cloud computing, co-simulation, message-oriented middleware, smart grid},\n  doi = {https://doi.org/10.1002/cpe.70238},\n  url = {https://onlinelibrary.wiley.com/doi/abs/10.1002/cpe.70238},\n  eprint = {https://onlinelibrary.wiley.com/doi/pdf/10.1002/cpe.70238},\n  abstract = {ABSTRACT The integration of renewable energy has driven the need for smart grid frameworks that enable efficient co-simulation, data management, and secure communication. This paper introduces CloudHive, a cloud-native framework designed to address these challenges by unifying large-scale power-network co-simulation, real-time data communication, and big data analytics in a single modular architecture. Unlike existing co-simulation tools or data platforms that operate in isolation, CloudHive uniquely enables bidirectional interaction between simulation environments (e.g., OpenDSS for power systems, OMNeT++ for communication networks) and real-world smart grids, supported by message-oriented middleware (RabbitMQ, Apache Kafka) for low-latency data exchange and Kubernetes for dynamic scalability. We evaluate CloudHive's accuracy, scalability, and usability through three representative case studies. The results show that CloudHive achieves high accuracy, performs well in real-world scenarios, and scales efficiently with growing workloads in cloud environments.},\n  year = {2025}\n}", "pdf": "pdf/Concurrency and Computation - 2025 - Kent - Cloudhive  A Cloud‐Based Framework for Smart Grid Co‐Simulation  Data  and.pdf"},
  'mcts-workflow': {"year": 2025, "bib": "@INPROCEEDINGS{11245283,\n  author={Zhao, Bocong and Cai, Mingyuan and Zhou, Mengbing and Wang, Yang},\n  booktitle={2025 IEEE International Symposium on Parallel and Distributed Processing with Applications (ISPA)},\n  title={A Monte Carlo Tree Search-Based Algorithm for Workflow Scheduling},\n  year={2025},\n  volume={},\n  number={},\n  pages={557-566},\n  keywords={Directed acyclic graph;Cloud computing;Monte Carlo methods;Uncertainty;Processor scheduling;Scheduling algorithms;Trees (botanical);Prototypes;Scheduling;Resource management;workflow;task scheduling;directed acyclic graph;Monte Carlo Tree Search},\n  doi={10.1109/ISPA67752.2025.00078}}", "pdf": "pdf/A_Monte_Carlo_Tree_Search-Based_Algorithm_for_Workflow_Scheduling.pdf"},
};

for (const [id, resource] of Object.entries(publicationResources)) {
  const paper = document.getElementById(id);
  if (!paper) continue;
  if (resource.year) {
    const year = paper.querySelector('.publication-year');
    year.textContent = String(resource.year);
    year.setAttribute('aria-label', `Publication year: ${resource.year}`);
    year.removeAttribute('title');
  }
  if (resource.bib.trim()) {
    const button = paper.querySelector('.bib-button');
    const panel = paper.querySelector('.bib-content');
    panel.querySelector('code').textContent = resource.bib;
    button.disabled = false;
    button.title = 'Show BibTeX';
    button.addEventListener('click', () => {
      panel.hidden = !panel.hidden;
      button.setAttribute('aria-expanded', String(!panel.hidden));
      button.title = panel.hidden ? 'Show BibTeX' : 'Hide BibTeX';
    });
  }
  if (resource.pdf) {
    const link = paper.querySelector('.pdf-link');
    link.href = resource.pdf;
    link.setAttribute('download', '');
    link.removeAttribute('aria-disabled');
    link.title = 'Download PDF';
  }
}

// Sort each publication group independently, newest years first.
// Equal years retain their existing order within that group.
for (const publicationList of document.querySelectorAll('.publication-list')) {
  const papers = Array.from(publicationList.children);
  papers.sort((a, b) =>
    (publicationResources[b.id]?.year || 0) - (publicationResources[a.id]?.year || 0)
  );
  papers.forEach((paper) => publicationList.append(paper));

  const pageSize = 5;
  let visibleCount = pageSize;
  if (papers.length > pageSize) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'news-toggle publication-more';
    button.textContent = 'Show more';
    if (!publicationList.id) {
      publicationList.id = publicationList.getAttribute('aria-labelledby').replace('-heading', '-list');
    }
    button.setAttribute('aria-controls', publicationList.id);
    const collapse = document.createElement('button');
    collapse.type = 'button';
    collapse.className = 'news-toggle publication-more';
    collapse.textContent = 'Show less';
    collapse.setAttribute('aria-controls', publicationList.id);
    const controls = document.createElement('div');
    controls.className = 'publication-controls';
    controls.append(button, collapse);
    const render = () => {
      papers.forEach((paper, index) => { paper.hidden = index >= visibleCount; });
      button.hidden = visibleCount >= papers.length;
      collapse.hidden = visibleCount <= pageSize;
    };
    button.addEventListener('click', () => {
      visibleCount += pageSize;
      render();
      if (button.hidden) collapse.focus({ preventScroll: true });
    });
    collapse.addEventListener('click', () => {
      visibleCount = pageSize;
      render();
      button.focus({ preventScroll: true });
    });
    render();
    publicationList.after(controls);
  }
}
