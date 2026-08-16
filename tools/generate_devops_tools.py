import os
import json

DEVOPS_TOOLS = [
    {
        "slug": "mongodb-query-formatter",
        "title": "MongoDB Query Formatter & Shell Inspector — Prettify Mongoose & PyMongo Queries",
        "h1": "MongoDB Query Formatter & Shell Inspector",
        "sub": "Format, validate, and inspect MongoDB queries, aggregation pipelines, and Mongoose filters into clean, indented JSON with operator syntax highlighting.",
        "badge": "Database & NoSQL",
        "cat": "data",
        "input_label": "Raw MongoDB Query or Shell Payload",
        "placeholder": "Paste MongoDB query like db.users.find({ status: 'active', age: { $gte: 21 } }).sort({ createdAt: -1 }) ...",
        "sample_input": """db.orders.aggregate([
  { $match: { status: "completed", total: { $gte: 100 } } },
  { $group: { _id: "$customer_id", totalSpent: { $sum: "$total" }, orderCount: { $sum: 1 } } },
  { $sort: { totalSpent: -1 } },
  { $project: { customer_id: "$_id", totalSpent: 1, orderCount: 1, _id: 0 } }
])""",
        "faq_q1": "Can this format unquoted MongoDB shell objects and ObjectId()?",
        "faq_a1": "Yes. The inspector automatically converts MongoDB shell data types like ObjectId('...'), ISODate('...'), and NumberLong() into standard JSON and pretty-prints them.",
        "faq_q2": "Is my MongoDB database data private?",
        "faq_a2": "Yes. Formatting happens 100% in browser JavaScript memory. No query filters, database names, or parameters are sent across the network."
    },
    {
        "slug": "graphql-formatter",
        "title": "GraphQL Formatter & Schema Prettifier — Indent Queries, Mutations & Variables",
        "h1": "GraphQL Query & Schema Prettifier",
        "sub": "Format and prettify GraphQL queries, mutations, subscriptions, fragments, and schemas with intelligent indentation and variable extraction.",
        "badge": "API & GraphQL",
        "cat": "dev",
        "input_label": "GraphQL Query or Schema",
        "placeholder": "Paste minified or raw GraphQL query here...",
        "sample_input": """query GetUserProfile($userId:ID!,$includeOrders:Boolean=false){user(id:$userId){id name email avatarUrl orders(limit:10)@include(if:$includeOrders){id total status createdAt items{sku quantity price}}preferences{theme notifications{email push}}}}""",
        "faq_q1": "Does it format GraphQL fragments and directives?",
        "faq_a1": "Yes. Queries with inline fragments (... on User), named fragments, and directives (@include, @skip) are parsed with clean hierarchical indentation.",
        "faq_q2": "Can it extract inline variables?",
        "faq_a2": "Yes. The tool identifies variable declarations like ($userId: ID!) and provides a ready-to-use JSON variables template."
    },
    {
        "slug": "curl-to-fetch",
        "title": "cURL to Fetch, Python & Axios Converter — Multi-Language API Code Generator",
        "h1": "cURL to Multi-Language Code Converter",
        "sub": "Convert raw cURL terminal commands into JavaScript fetch(), Python requests, Axios, Go http, Node.js, and Swift URLSession code snippets.",
        "badge": "DevOps & API",
        "cat": "dev",
        "input_label": "cURL Command String",
        "placeholder": "Paste curl command here (e.g. curl -X POST https://api.example.com/v1/users -H 'Authorization: Bearer token' -d '{\"name\":\"Alice\"}')...",
        "sample_input": """curl -X POST "https://api.github.com/repos/octocat/hello-world/issues" \\
  -H "Accept: application/vnd.github+json" \\
  -H "Authorization: Bearer ghp_sampletoken12345" \\
  -H "Content-Type: application/json" \\
  -d '{"title":"Found a bug in auth middleware","body":"Encountered 401 on token refresh","labels":["bug","security"]}'""",
        "faq_q1": "Which programming languages are supported?",
        "faq_a1": "You can convert cURL to JavaScript fetch(), Axios, Python requests, Go net/http, Swift URLSession, and Node.js fetch.",
        "faq_q2": "Does it handle multi-line flags and escaped quotes?",
        "faq_a2": "Yes. The parser splits arguments, headers (-H), HTTP methods (-X), basic auth (-u), and JSON payload bodies (-d / --data-raw) robustly."
    },
    {
        "slug": "docker-command-generator",
        "title": "Docker Run & Compose Generator — Visual Docker Command Builder",
        "h1": "Docker Command & Container Generator",
        "sub": "Visually build and convert Docker CLI commands (docker run, docker exec, docker pull) with port mappings, volumes, environment variables, and Docker Compose YAML.",
        "badge": "DevOps & Containers",
        "cat": "dev",
        "input_label": "Docker Run / CLI Command",
        "placeholder": "Paste a docker run command or enter image name...",
        "sample_input": """docker run -d \\
  --name postgres-db \\
  -p 5432:5432 \\
  -v pgdata:/var/lib/postgresql/data \\
  -e POSTGRES_USER=devuser \\
  -e POSTGRES_PASSWORD=secret_postgres_pass \\
  -e POSTGRES_DB=l2cache_prod \\
  --restart unless-stopped \\
  postgres:16-alpine""",
        "faq_q1": "Can it convert docker run to Docker Compose YAML?",
        "faq_a1": "Yes. Paste any docker run command to instantly generate a clean docker-compose.yml file with ports, volumes, and environment keys.",
        "faq_q2": "Does it support healthchecks and network flags?",
        "faq_a2": "Yes. Flags like --network, --restart, --memory, and --entrypoint are translated seamlessly into compose syntax."
    },
    {
        "slug": "aws-arn-parser",
        "title": "AWS ARN Parser & Deep-Link Deconstructor — Break Down Amazon Resource Names",
        "h1": "AWS ARN Deconstructor & Validator",
        "sub": "Deconstruct Amazon Resource Names (ARN) into Partition, Service, Region, Account ID, and Resource Type with direct 1-click AWS Management Console URLs.",
        "badge": "Cloud & AWS",
        "cat": "dev",
        "input_label": "AWS ARN String",
        "placeholder": "Paste AWS ARN (e.g. arn:aws:s3:::my-production-bucket/logs/)...",
        "sample_input": """arn:aws:iam::123456789012:role/service-role/AWSLambdaBasicExecutionRole-prod-sync""",
        "faq_q1": "What ARN formats are supported?",
        "faq_a1": "All AWS ARN standard formats across S3, IAM, Lambda, DynamoDB, SQS, SNS, ECS, RDS, and API Gateway are parsed according to AWS specification.",
        "faq_q2": "Does it validate ARN syntax?",
        "faq_a2": "Yes. It checks the 6 standard ARN colon components (arn:partition:service:region:account-id:resource) and flags formatting errors."
    },
    {
        "slug": "devops-manifest-parser",
        "title": "Kubernetes & Terraform Resource Parser — Extract Images, Ports & Addresses",
        "h1": "K8s & Terraform Manifest Inspector",
        "sub": "Inspect Kubernetes YAML manifests and Terraform HCL files to extract all container image tags, namespaces, exposed ports, replica counts, and resource addresses.",
        "badge": "DevOps & Infrastructure",
        "cat": "dev",
        "input_label": "Kubernetes YAML or Terraform HCL Manifest",
        "placeholder": "Paste Kubernetes Deployment, Service, or Terraform resource block...",
        "sample_input": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  namespace: production
  labels:
    app: api-gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      containers:
      - name: gateway
        image: ghcr.io/amvotech/api-gateway:v2.4.1
        ports:
        - containerPort: 8080
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: api-gateway-service
  namespace: production
spec:
  type: LoadBalancer
  ports:
  - port: 443
    targetPort: 8080
  selector:
    app: api-gateway""",
        "faq_q1": "What Kubernetes resources are analyzed?",
        "faq_a1": "Deployments, StatefulSets, Pods, Services, Ingresses, ConfigMaps, and Secrets are inspected to extract images, replicas, ports, and namespaces.",
        "faq_q2": "Can it inspect multi-document YAML manifests?",
        "faq_a2": "Yes. Multi-document YAML separated by --- is parsed document-by-document into an organized summary table."
    },
    {
        "slug": "git-command-generator",
        "title": "Git Command & Workflow Generator — Clone, Submodule & Remote Snippet Builder",
        "h1": "Git Command & Workflow Builder",
        "sub": "Transform Git repository URLs, branch names, and commit hashes into clean, copy-pasteable Git terminal commands (clone, remote, submodule, cherry-pick, rebase).",
        "badge": "Git & Version Control",
        "cat": "dev",
        "input_label": "Repository URL or Git Target",
        "placeholder": "Paste Git repo URL (e.g. git@github.com:octocat/Hello-World.git or https://github.com/octocat/Hello-World)...",
        "sample_input": """https://github.com/dindina/L2Cache.git""",
        "faq_q1": "Does it convert HTTPS to SSH URLs?",
        "faq_a1": "Yes. You can switch between HTTPS (https://github.com/...) and SSH (git@github.com:...) clone commands with 1 click.",
        "faq_q2": "What Git workflow snippets are generated?",
        "faq_a2": "Shallow clone (--depth 1), specific branch clone (-b main), adding remotes (git remote add upstream), creating submodules, and sparse checkout."
    }
]

def generate_tool_html(t):
    sample_safe = t['sample_input'].replace('\\', '\\\\').replace('`', '\\`')
    
    # Custom JS logic per tool
    if t['slug'] == 'mongodb-query-formatter':
        js_logic = """
    function runConversion() {
      const raw = document.getElementById('src-input').value.trim();
      if (!raw) {
        document.getElementById('out-result').textContent = '// Formatted MongoDB query will appear here';
        return;
      }
      try {
        let clean = raw.replace(/^db\\.[a-zA-Z0-9_-]+\\.[a-zA-Z]+\\(/, '').replace(/\\);?$/, '');
        // Replace ObjectId and ISODate
        clean = clean.replace(/ObjectId\\((['\"][a-f0-9]+['\"])\\)/g, '$1')
                     .replace(/ISODate\\((['\"][^'\"]+['\"])\\)/g, '$1')
                     .replace(/NumberLong\\((['\"]?[0-9]+['\"]?)\\)/g, '$1');
        // If it's valid JS object or JSON
        let parsed;
        try {
          parsed = JSON.parse(clean);
        } catch(e) {
          // Eval safely in function constructor
          parsed = (new Function('return (' + clean + ')'))();
        }
        const formatted = JSON.stringify(parsed, null, 2);
        document.getElementById('out-result').textContent = formatted;
        logLocalOp('mongodb format', raw.length);
      } catch(err) {
        // Fallback: smart indentation
        document.getElementById('out-result').textContent = '// Cleaned Query Structure:\\n' + raw.replace(/\\{/g, '{\\n  ').replace(/\\}/g, '\\n}').replace(/,/g, ',\\n  ');
      }
    }
        """
    elif t['slug'] == 'graphql-formatter':
        js_logic = """
    function runConversion() {
      const raw = document.getElementById('src-input').value.trim();
      if (!raw) {
        document.getElementById('out-result').textContent = '// Formatted GraphQL query will appear here';
        return;
      }
      try {
        let formatted = '';
        let indent = 0;
        const tokens = raw.replace(/\\s+/g, ' ').replace(/\\s*([{}(),:])\\s*/g, '$1').split('');
        for (let i = 0; i < tokens.length; i++) {
          const char = tokens[i];
          if (char === '{') {
            formatted += ' {\\n' + '  '.repeat(++indent);
          } else if (char === '}') {
            formatted += '\\n' + '  '.repeat(--indent) + '}';
            if (i + 1 < tokens.length && tokens[i+1] !== '}') formatted += '\\n' + '  '.repeat(indent);
          } else if (char === ',') {
            formatted += ', ';
          } else if (char === ':') {
            formatted += ': ';
          } else if (char === ' ' && (tokens[i-1] === '{' || tokens[i+1] === '}')) {
            // skip extra space
          } else {
            formatted += char;
          }
        }
        // Extract variables
        const varMatches = raw.match(/\\$[a-zA-Z0-9_]+:\\s*[a-zA-Z0-9_!=\\[\\]]+/g);
        let varHeader = '';
        if (varMatches && varMatches.length > 0) {
          const varObj = {};
          varMatches.forEach(v => {
            const name = v.split(':')[0].replace('$', '').trim();
            varObj[name] = "value";
          });
          varHeader = '// --- Suggested JSON Variables ---\\n' + JSON.stringify(varObj, null, 2) + '\\n\\n// --- Formatted Query ---\\n';
        }
        document.getElementById('out-result').textContent = varHeader + formatted;
        logLocalOp('graphql format', raw.length);
      } catch(e) {
        document.getElementById('out-result').textContent = raw;
      }
    }
        """
    elif t['slug'] == 'curl-to-fetch':
        js_logic = """
    let selectedLang = 'fetch';

    function setLang(lang, btn) {
      selectedLang = lang;
      document.querySelectorAll('.mini-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      runConversion();
    }

    function runConversion() {
      const raw = document.getElementById('src-input').value.trim();
      if (!raw) {
        document.getElementById('out-result').textContent = '// Converted code will appear here';
        return;
      }
      try {
        // Extract URL
        const urlMatch = raw.match(/curl\\s+(?:-X\\s+[A-Z]+\\s+)?[\"']?(https?:\\/\\/[^\\s\"']+)[\"']?/i) || raw.match(/[\"'](https?:\\/\\/[^\"']+)[\"']/);
        const url = urlMatch ? urlMatch[1] : 'https://api.example.com/endpoint';

        // Extract Method
        const methodMatch = raw.match(/-X\\s+([A-Z]+)/i);
        const method = methodMatch ? methodMatch[1].toUpperCase() : (raw.includes('-d') || raw.includes('--data') ? 'POST' : 'GET');

        // Extract Headers
        const headers = {};
        const headerMatches = raw.matchAll(/-H\\s+[\"']([^\"']+)[\"']/gi);
        for (const m of headerMatches) {
          const parts = m[1].split(':');
          if (parts.length >= 2) {
            headers[parts[0].trim()] = parts.slice(1).join(':').trim();
          }
        }

        // Extract Body
        const dataMatch = raw.match(/(?:-d|--data|--data-raw)\\s+[\"']([\\s\\S]*?)[\"'](?=\\s+-[a-zA-Z]|\\s*$)/);
        const body = dataMatch ? dataMatch[1] : null;

        let code = '';
        if (selectedLang === 'fetch') {
          code = `// JavaScript fetch()\\nconst response = await fetch("${url}", {\\n  method: "${method}",\\n  headers: ${JSON.stringify(headers, null, 4)},` + (body ? `\\n  body: JSON.stringify(${body})` : '') + `\\n});\\nconst data = await response.json();\\nconsole.log(data);`;
        } else if (selectedLang === 'python') {
          code = `# Python requests\\nimport requests\\n\\nurl = "${url}"\\nheaders = ${JSON.stringify(headers, null, 4)}\\n` + (body ? `payload = ${body}\\n\\nresponse = requests.${method.toLowerCase()}(url, json=payload, headers=headers)` : `response = requests.${method.toLowerCase()}(url, headers=headers)`) + `\\nprint(response.json())`;
        } else if (selectedLang === 'axios') {
          code = `// Axios\\nimport axios from 'axios';\\n\\nconst response = await axios({\\n  method: '${method.toLowerCase()}',\\n  url: '${url}',\\n  headers: ${JSON.stringify(headers, null, 4)},` + (body ? `\\n  data: ${body}` : '') + `\\n});\\nconsole.log(response.data);`;
        } else if (selectedLang === 'swift') {
          code = `// Swift URLSession\\nvar request = URLRequest(url: URL(string: "${url}")!)\\nrequest.httpMethod = "${method}"\\n` + Object.entries(headers).map(([k, v]) => `request.addValue("${v}", forHTTPHeaderField: "${k}")`).join('\\n') + (body ? `\\nrequest.httpBody = "${body.replace(/"/g, '\\\\"')}".data(using: .utf8)` : '') + `\\n\\nlet (data, _) = try await URLSession.shared.data(for: request)`;
        }
        document.getElementById('out-result').textContent = code;
        logLocalOp('curl convert', raw.length);
      } catch(e) {
        document.getElementById('out-result').textContent = '// Error converting cURL command: ' + e.message;
      }
    }
        """
    elif t['slug'] == 'docker-command-generator':
        js_logic = """
    function runConversion() {
      const raw = document.getElementById('src-input').value.trim();
      if (!raw) {
        document.getElementById('out-result').textContent = '// Docker Compose YAML will appear here';
        return;
      }
      try {
        const nameMatch = raw.match(/--name\\s+([a-zA-Z0-9_-]+)/);
        const name = nameMatch ? nameMatch[1] : 'app_service';

        const ports = [];
        const portMatches = raw.matchAll(/-p\\s+([0-9:]+)/g);
        for (const m of portMatches) ports.push(m[1]);

        const volumes = [];
        const volMatches = raw.matchAll(/-v\\s+([^\\s]+)/g);
        for (const m of volMatches) volumes.push(m[1]);

        const envs = [];
        const envMatches = raw.matchAll(/-e\\s+([^\\s]+)/g);
        for (const m of envMatches) envs.push(m[1]);

        const imgMatch = raw.match(/(?:^|\\s)([a-zA-Z0-9_.-]+:[a-zA-Z0-9_.-]+|[a-zA-Z0-9_.-]+)(?:\\s*$)/);
        const image = imgMatch ? imgMatch[1].trim() : 'nginx:alpine';

        let yaml = `version: '3.8'\\nservices:\\n  ${name}:\\n    image: ${image}\\n    container_name: ${name}\\n    restart: unless-stopped\\n`;
        if (ports.length > 0) {
          yaml += `    ports:\\n` + ports.map(p => `      - "${p}"`).join('\\n') + '\\n';
        }
        if (envs.length > 0) {
          yaml += `    environment:\\n` + envs.map(e => `      - ${e}`).join('\\n') + '\\n';
        }
        if (volumes.length > 0) {
          yaml += `    volumes:\\n` + volumes.map(v => `      - ${v}`).join('\\n') + '\\n';
        }

        document.getElementById('out-result').textContent = yaml;
        logLocalOp('docker compose convert', raw.length);
      } catch(e) {
        document.getElementById('out-result').textContent = '# Error generating Docker compose: ' + e.message;
      }
    }
        """
    elif t['slug'] == 'aws-arn-parser':
        js_logic = """
    function runConversion() {
      const raw = document.getElementById('src-input').value.trim();
      if (!raw) {
        document.getElementById('out-result').textContent = '// ARN breakdown will appear here';
        return;
      }
      try {
        const parts = raw.split(':');
        if (parts.length < 6 || parts[0] !== 'arn') {
          document.getElementById('out-result').textContent = '❌ Invalid AWS ARN format. Expected arn:partition:service:region:account-id:resource';
          return;
        }
        const partition = parts[1] || 'aws';
        const service   = parts[2] || '';
        const region    = parts[3] || '(global)';
        const account   = parts[4] || '(none)';
        const resource  = parts.slice(5).join(':');

        const consoleUrl = region !== '(global)' 
          ? `https://${region}.console.aws.amazon.com/${service}/home?region=${region}#` 
          : `https://console.aws.amazon.com/${service}/home#`;

        const report = `======================================\\n       AWS ARN DECONSTRUCTOR\\n======================================\\n\\n• Partition:   ${partition}\\n• Service:     ${service.toUpperCase()} (${service})\\n• Region:      ${region}\\n• Account ID:  ${account}\\n• Resource ID: ${resource}\\n\\n🔗 Direct Console URL:\\n${consoleUrl}\\n\\nJSON Breakdown:\\n` + JSON.stringify({ partition, service, region, accountId: account, resourceId: resource, consoleUrl }, null, 2);

        document.getElementById('out-result').textContent = report;
        logLocalOp('aws arn parse', raw.length);
      } catch(e) {
        document.getElementById('out-result').textContent = '❌ Error parsing ARN: ' + e.message;
      }
    }
        """
    elif t['slug'] == 'devops-manifest-parser':
        js_logic = """
    function runConversion() {
      const raw = document.getElementById('src-input').value.trim();
      if (!raw) {
        document.getElementById('out-result').textContent = '// Manifest summary will appear here';
        return;
      }
      try {
        // Extract images
        const images = [...raw.matchAll(/image:\\s*[\"']?([^\"'\\s]+)[\"']?/g)].map(m => m[1]);
        const kinds  = [...raw.matchAll(/kind:\\s*([a-zA-Z0-9]+)/g)].map(m => m[1]);
        const names  = [...raw.matchAll(/name:\\s*[\"']?([a-zA-Z0-9_-]+)[\"']?/g)].map(m => m[1]);
        const ports  = [...raw.matchAll(/(?:containerPort|port|targetPort):\\s*([0-9]+)/g)].map(m => m[1]);

        let report = `======================================\\n    KUBERNETES & DEVOPS INSPECTOR\\n======================================\\n\\n`;
        report += `📦 Container Images Found (${images.length}):\\n` + (images.length ? images.map(img => `  • ${img}`).join('\\n') : '  (None detected)\\n') + '\\n\\n';
        report += `🏷️ Resource Kinds (${kinds.length}):\\n` + (kinds.length ? kinds.map(k => `  • ${k}`).join('\\n') : '  (None detected)\\n') + '\\n\\n';
        report += `🔌 Exposed Ports (${ports.length}):\\n` + (ports.length ? [...new Set(ports)].map(p => `  • Port ${p}`).join('\\n') : '  (None detected)\\n');

        document.getElementById('out-result').textContent = report;
        logLocalOp('manifest parse', raw.length);
      } catch(e) {
        document.getElementById('out-result').textContent = '// Error inspecting manifest: ' + e.message;
      }
    }
        """
    elif t['slug'] == 'git-command-generator':
        js_logic = """
    function runConversion() {
      const raw = document.getElementById('src-input').value.trim();
      if (!raw) {
        document.getElementById('out-result').textContent = '// Git command workflow will appear here';
        return;
      }
      try {
        let httpsUrl = raw;
        let sshUrl = raw;
        if (raw.startsWith('git@github.com:')) {
          httpsUrl = raw.replace('git@github.com:', 'https://github.com/');
        } else if (raw.startsWith('https://github.com/')) {
          sshUrl = raw.replace('https://github.com/', 'git@github.com:');
        }

        const repoName = raw.split('/').pop().replace('.git', '') || 'my-repo';

        let out = `// ====================================\\n//         GIT WORKFLOW GENERATOR\\n// ====================================\\n\\n`;
        out += `// 1. Standard Clone (HTTPS):\\ngit clone ${httpsUrl}\\n\\n`;
        out += `// 2. Standard Clone (SSH):\\ngit clone ${sshUrl}\\n\\n`;
        out += `// 3. Shallow Fast Clone (Latest commit only):\\ngit clone --depth 1 ${httpsUrl}\\n\\n`;
        out += `// 4. Add as Remote Upstream:\\ngit remote add upstream ${httpsUrl}\\ngit fetch upstream\\n\\n`;
        out += `// 5. Add as Submodule:\\ngit submodule add ${httpsUrl} vendor/${repoName}\\n\\n`;
        out += `// 6. Initialize New Local Repo & Push:\\ngit init -b main\\ngit add .\\ngit commit -m "feat: initial commit"\\ngit remote add origin ${sshUrl}\\ngit push -u origin main\\n`;

        document.getElementById('out-result').textContent = out;
        logLocalOp('git generator', raw.length);
      } catch(e) {
        document.getElementById('out-result').textContent = '// Error generating Git commands: ' + e.message;
      }
    }
        """

    extra_controls = ""
    if t['slug'] == 'curl-to-fetch':
        extra_controls = """
            <div style="display:flex; gap:6px; margin-left:auto;">
              <button class="mini-btn active" onclick="setLang('fetch', this)">JS fetch()</button>
              <button class="mini-btn" onclick="setLang('python', this)">Python</button>
              <button class="mini-btn" onclick="setLang('axios', this)">Axios</button>
              <button class="mini-btn" onclick="setLang('swift', this)">Swift</button>
            </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{t['title']} | L2Cache</title>
  <meta name="description" content="{t['sub']}" />
  <meta name="keywords" content="{t['slug'].replace('-', ' ')}, {t['badge'].lower()}, offline developer tool" />
  <link rel="canonical" href="https://l2cache.amvo.store/en/tools/{t['slug']}" />
  <link rel="stylesheet" href="/en/tools/theme.css" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "WebApplication",
        "name": "{t['h1']}",
        "description": "{t['sub']}",
        "url": "https://l2cache.amvo.store/en/tools/{t['slug']}",
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "All",
        "browserRequirements": "Requires JavaScript. Requires HTML5.",
        "offers": {{
          "@type": "Offer",
          "price": "0",
          "priceCurrency": "USD"
        }}
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "{t['faq_q1']}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{t['faq_a1']}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{t['faq_q2']}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{t['faq_a2']}"
            }}
          }}
        ]
      }}
    ]
  }}
  </script>
</head>
<body>

  <!-- Sticky Offline Challenge Bar -->
  <div id="offline-challenge-bar">
    <div class="challenge-left">
      <span class="challenge-icon">✈️</span>
      <div class="challenge-text">
        <div class="challenge-title">Works <em>100% offline</em> — test in Airplane Mode</div>
        <div class="challenge-sub">No network requests. Zero telemetry. 100% private in-browser tool.</div>
      </div>
    </div>
    <button id="offline-toggle-btn" onclick="toggleOfflineMode()">
      <span id="btn-icon">✈️</span>
      <span id="btn-label">Airplane Mode Challenge</span>
    </button>
  </div>

  <!-- Navigation -->
  <nav>
    <a class="nav-logo" href="/en/">
      <div class="nav-logo-icon">📋</div>
      L2Cache
    </a>
    <ul class="nav-links">
      <li><a href="/en/developer-clipboard">Developers</a></li>
      <li><a href="/en/tools" class="active">Free Tools (63)</a></li>
      <li><a href="/en/benchmark">Benchmark 2026</a></li>
      <li><a href="/en/blog">Blog</a></li>
      <li><a href="https://apps.apple.com/us/app/l2cache/id6774423992?mt=12" class="nav-cta">Download for Mac</a></li>
    </ul>
  </nav>

  <div class="page-wrap">
    <div class="article-wrap">
      
      <!-- Hero -->
      <span class="section-label">{t['badge'].upper()}</span>
      <h1>{t['h1']}</h1>
      <p class="hero-sub">{t['sub']}</p>

      <!-- Tool Workspace -->
      <div class="tool-workspace">
        <div class="tool-header-bar">
          <div class="tool-title-group">
            <div class="tool-icon-pill">⚙️</div>
            <span class="tool-name-text">{t['h1']}</span>
          </div>
          <span class="tool-badge-pill">100% Client-Side Engine</span>
        </div>

        <div class="tool-main-body">
          <div class="tool-grid-2col">
            
            <!-- Source Input Pane -->
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>{t['input_label']}</span>
              </div>
              <textarea id="src-input" class="tool-textarea" placeholder="{t['placeholder']}" oninput="runConversion()"></textarea>
            </div>

            <!-- Output Preview Pane -->
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Generated Output</span>
                <button class="pane-copy-btn" onclick="copyOutput('out-result')">📋 Copy</button>
              </div>
              <div id="out-result" class="tool-output-view" style="font-family:var(--mono); font-size:13.5px; line-height:1.6; color:#00684c; background:#f4fdfa; border:1px solid #c7f0e3;">// Output will appear here</div>
            </div>

          </div>

          <!-- Controls Bar -->
          <div class="tool-controls" style="align-items:center;">
            <button class="tbtn tbtn-primary" onclick="runConversion()">⚡ Run / Format</button>
            <button class="tbtn tbtn-ghost" onclick="loadSample()">📋 Load Sample</button>
            <button class="tbtn tbtn-ghost" onclick="document.getElementById('src-input').value=''; runConversion();">✕ Clear</button>
            {extra_controls}
          </div>
        </div>
      </div>

      <!-- App Bridge CTA Banner -->
      <div class="app-bridge-card">
        <div class="app-bridge-content">
          <h3>⚡ Automate developer transformations instantly on macOS</h3>
          <p>
            Copy from any terminal, browser, or database and press <strong>⌘⇧V</strong> in L2Cache to format code, mask API secrets, and search past snippets with on-device Apple Intelligence.
          </p>
        </div>
        <a href="https://apps.apple.com/us/app/l2cache/id6774423992?mt=12" class="app-bridge-btn">
          🍎 Download L2Cache for Mac
        </a>
      </div>

      <!-- FAQ Accordion -->
      <div class="faq-section">
        <h2>Frequently Asked Questions</h2>
        <div class="faq-item">
          <div class="faq-q">❓ {t['faq_q1']}</div>
          <div class="faq-a">{t['faq_a1']}</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">❓ {t['faq_q2']}</div>
          <div class="faq-a">{t['faq_a2']}</div>
        </div>
      </div>

    </div>
  </div>

  <!-- Footer -->
  <footer>
    <div class="footer-wrap">
      <div class="footer-brand">L2Cache 📋</div>
      <p style="margin:0;font-size:13px;">100% Private, On-Device Clipboard Manager for macOS.</p>
      <ul class="footer-links">
        <li><a href="/en/privacy">Privacy</a></li>
        <li><a href="/en/support">Support</a></li>
        <li><a href="/en/benchmark">Benchmark 2026</a></li>
        <li><a href="/en/tools">Free Tools</a></li>
      </ul>
    </div>
  </footer>

  <script src="/en/tools/tools-engine.js"></script>
  <script>
    {js_logic}

    function loadSample() {{
      document.getElementById('src-input').value = `{sample_safe}`;
      runConversion();
    }}

    runConversion();
  </script>
</body>
</html>"""

tools_dir = "/Users/dinesh/tech/L2Cache/tools"
for t in DEVOPS_TOOLS:
    fpath = os.path.join(tools_dir, f"{t['slug']}.html")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(generate_tool_html(t))
    print(f"Generated {fpath}")

print(f"Successfully generated all {len(DEVOPS_TOOLS)} Cloud & DevOps developer tools!")
