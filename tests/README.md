# NAME - Name Generation System

A comprehensive AI-powered name generation system that creates culturally appropriate identities using advanced AI agents, MCP (Multi-Agent Communication Protocol) integration, and a modern React frontend.

## 🏗️ System Architecture

```mermaid
graph TB
    %% Frontend Layer
    subgraph "Frontend Layer"
        UI[React Frontend<br/>Material-UI<br/>Port 3000]
        UI -->|HTTP Requests| COMBINED
    end
    
    %% Combined Service Layer
    subgraph "Combined Service Layer"
        COMBINED[Combined MCP + API Service<br/>Port 8500<br/>FastAPI + MCP Protocol]
        COMBINED -->|MCP Tools| MCP_TOOLS[Weight Templates<br/>Culture Overrides<br/>Validate Weights<br/>Generate Identity]
        COMBINED -->|REST API| API_ENDPOINTS[Generate Identity<br/>Categories<br/>Weight Management<br/>Health Check]
    end
    
    %% Core Logic Layer
    subgraph "Core Logic Layer"
        WG[Weight Configuration<br/>YAML Config<br/>Culture Overrides<br/>Templates]
        NG[Name Generator<br/>Cultural Context<br/>Weighted Selection]
        WC[Weight Config<br/>Validation<br/>Normalization]
    end
    
    %% AI Layer
    subgraph "AI Layer"
        SA[Strands Agents<br/>Cultural Analyst<br/>Linguistic Expert<br/>Validation Agent]
        SA -->|LLM Calls| OLLAMA[Ollama<br/>Local LLM]
    end
    
    %% Database Layer
    subgraph "Database Layer"
        DB[(SQLite Database<br/>name_generation.db<br/>User Preferences<br/>Weight History)]
    end
    
    %% External Services
    subgraph "External Services"
        OLLAMA
        EXTERNAL[External APIs<br/>Domain Services<br/>Cultural Databases]
    end
    
    %% Data Flow
    UI -.->|User Input| COMBINED
    COMBINED -.->|Weight Config| WG
    COMBINED -.->|Name Generation| NG
    NG -.->|Cultural Context| SA
    SA -.->|Store Results| DB
    COMBINED -.->|Return Names| UI
    WG -.->|Validation| WC
    
    %% Styling
    classDef frontend fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef combined fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef core fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef ai fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef database fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef external fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    
    class UI frontend
    class COMBINED,MCP_TOOLS,API_ENDPOINTS combined
    class WG,NG,WC core
    class SA ai
    class DB database
    class OLLAMA,EXTERNAL external
```

## ✨ Features

### 🎯 Core Capabilities
- **Cultural Name Generation**: Generate names appropriate for specific ethnicities and regions
- **Multi-Agent AI System**: Uses specialized AI agents for cultural analysis, linguistic expertise, and validation
- **MCP Integration**: Full Multi-Agent Communication Protocol support with external tools
- **Fast Mode**: Quick generation using pre-defined culturally appropriate name pools
- **Swarm Mode**: Advanced generation using AI agent swarms for complex scenarios
- **Real-time Validation**: Domain availability, trademark checks, and cultural context validation

### 🌍 Supported Cultures
- **Asian**: Cambodian, Chinese, Japanese, Korean, Vietnamese, Indian, Taiwanese
- **Western**: American, European, Caucasian
- **Hispanic**: Spanish, Latin American
- **African**: Black, African American
- **Mixed**: Multi-cultural identities

### 🔧 Technical Features
- **React Frontend**: Modern UI with Material-UI components
- **FastAPI Backend**: High-performance API with automatic documentation
- **SQLite Database**: Lightweight persistence layer
- **Ollama Integration**: Local LLM processing
- **Dynamic Port Management**: Automatic port conflict resolution
- **Comprehensive Logging**: Detailed traceability and debugging

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+
- Ollama (for local LLM processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/goagiq/NAME.git
   cd NAME
   ```

2. **Install Python dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Start the system**
   ```bash
   # Start combined service (MCP + API on port 8500)
   .venv/Scripts/python.exe start_combined_service.py
   
   # In a new terminal, start the frontend
   cd frontend
   npm start
   ```

## 📖 Usage

### Web Interface
1. Open your browser to `http://localhost:3000`
2. Fill out the identity generation form:
   - **Sex**: Male/Female
   - **Location**: Country/Region
   - **Age**: Age range
   - **Occupation**: Professional field
   - **Race**: Ethnicity
   - **Religion**: Religious background (optional)
   - **Birth Year**: Year of birth (optional)
3. Click "Generate Identity" to create 5 culturally appropriate names
4. Use "Regenerate" to get new names

### API Usage

#### Generate Names
```bash
curl -X POST "http://localhost:8500/api/generate-identity" \
  -H "Content-Type: application/json" \
  -d '{
    "sex": "Female",
    "location": "USA",
    "age": 25,
    "occupation": "Engineer",
    "race": "Asian",
    "religion": "Buddhist",
    "birth_year": 1998,
    "custom_weights": {
      "race": 0.30,
      "location": 0.20,
      "age": 0.15
    },
    "template_name": "cultural_focus"
  }'
```

#### Check System Health
```bash
curl "http://localhost:8500/health"
```

#### Get Available Categories
```bash
curl "http://localhost:8500/api/categories"
```

#### Get Weight Templates
```bash
curl "http://localhost:8500/api/weights/templates"
```

#### Validate Weights
```bash
curl -X POST "http://localhost:8500/api/weights/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "field_weights": {
      "sex": 0.25,
      "location": 0.20,
      "age": 0.15,
      "occupation": 0.10,
      "race": 0.20,
      "religion": 0.05,
      "birth_year": 0.05
    }
  }'
```

### MCP Integration

The system includes a full MCP server on port 8500 with the following tools:

- **generate_identity**: Generate culturally appropriate identities with configurable weights
- **get_weight_templates**: Get available weight templates
- **get_culture_overrides**: Get culture-specific weight overrides
- **validate_weights**: Validate weight configuration

```bash
# Test MCP connectivity
.venv/Scripts/python.exe test_mcp_client.py

# Test MCP tools directly
curl -X POST http://localhost:8500/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

## 🔧 Configuration

### Port Configuration
- **Combined Service**: Port 8500 (MCP + API)
- **Frontend**: Port 3000

### Environment Variables
```bash
# Database configuration
DATABASE_URL=sqlite:///name_generation.db

# Logging level
LOG_LEVEL=INFO

# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
```

## ⚙️ Configuration System

### Weight Configuration (`src/config/field_weights.yaml`)

The system uses a sophisticated weight configuration system that allows fine-tuning of input field importance for name generation. This configuration is stored in YAML format and supports multiple levels of customization.

#### Default Weights
```yaml
field_weights:
  default:
    sex: 0.25              # Gender (25% importance)
    location: 0.20         # Geographic location (20% importance)
    age: 0.15              # Age range (15% importance)
    occupation: 0.10       # Professional field (10% importance)
    race: 0.20             # Ethnicity/culture (20% importance)
    religion: 0.05         # Religious background (5% importance)
    birth_year: 0.05       # Birth year (5% importance)
    birth_country: 0.02    # Country of birth (2% importance)
    citizenship_country: 0.01  # Current citizenship (1% importance)
    diaspora_generation: 0.01  # Immigrant generation (1% importance)
```

#### Culture-Specific Overrides
The system supports culture-specific weight adjustments to better reflect the importance of certain fields for different ethnicities:

```yaml
culture_overrides:
  chinese:
    race: 0.30             # Higher emphasis on ethnicity
    location: 0.15         # Reduced location importance
    birth_year: 0.08       # Increased birth year importance
  
  spanish:
    location: 0.25         # Higher emphasis on location
    religion: 0.10         # Increased religion importance
    birth_country: 0.05    # Birth country more important
  
  indian:
    race: 0.28             # High ethnicity importance
    religion: 0.12         # Religion more significant
    birth_country: 0.04    # Birth country consideration
```

**Supported Cultures:**
- **Asian**: chinese, japanese, korean, vietnamese, thai, filipino, indian
- **Hispanic**: spanish, arabic, persian, turkish
- **African**: african_american, african
- **European**: eastern_european, scandinavian, italian, french
- **American**: american

#### Weight Templates
Pre-configured templates for common use cases:

```yaml
templates:
  cultural_focus:
    description: "Emphasize cultural and ethnic background"
    weights:
      race: 0.35           # High ethnicity emphasis
      location: 0.20       # Moderate location
      sex: 0.20            # Moderate gender
      age: 0.10            # Lower age importance
      occupation: 0.08     # Lower occupation importance
      religion: 0.05       # Minimal religion
      birth_year: 0.02     # Minimal birth year

  geographic_focus:
    description: "Emphasize location and regional context"
    weights:
      location: 0.35       # High location emphasis
      race: 0.20           # Moderate ethnicity
      sex: 0.20            # Moderate gender
      age: 0.12            # Moderate age
      occupation: 0.08     # Lower occupation
      religion: 0.03       # Minimal religion
      birth_year: 0.02     # Minimal birth year

  professional_focus:
    description: "Emphasize occupation and professional context"
    weights:
      occupation: 0.30     # High occupation emphasis
      sex: 0.25            # High gender importance
      location: 0.20       # Moderate location
      age: 0.15            # Moderate age
      race: 0.10           # Lower ethnicity importance

  balanced:
    description: "Balanced approach for general use"
    weights:
      sex: 0.25            # Equal gender importance
      location: 0.20       # Equal location importance
      age: 0.15            # Moderate age
      occupation: 0.10     # Lower occupation
      race: 0.20           # Equal ethnicity importance
      religion: 0.05       # Minimal religion
      birth_year: 0.05     # Minimal birth year
```

#### Validation Rules
The system includes comprehensive validation to ensure weight configurations are valid:

```yaml
validation:
  min_weight: 0.01         # Minimum weight per field
  max_weight: 0.50         # Maximum weight per field
  total_weight_range: [0.8, 1.2]  # Total weights should be between 0.8-1.2
  required_fields: ["sex", "location", "age", "occupation", "race"]
```

### Service Configuration

#### MCP Service Configuration
```yaml
mcp:
  host: localhost
  port: 8500
  log_level: INFO
```

#### API Service Configuration
```yaml
api:
  host: localhost
  port: 8001
  log_level: INFO
  cors_origins: ["http://localhost:3000"]
  enable_docs: true
```

### Configuration Management

#### Loading Configuration
The system uses a centralized configuration management system:

```python
from src.config import get_field_weights, get_service_config

# Get weight configuration
weights = get_field_weights()

# Get service configuration
mcp_config = get_service_config('mcp')
api_config = get_service_config('api')
```

#### Dynamic Weight Application
Weights are applied in the following order (later overrides earlier):

1. **Default weights** from configuration
2. **Culture-specific overrides** (if culture is specified)
3. **Template weights** (if template is specified)
4. **User custom weights** (if provided in request)
5. **Request-specific weights** (if provided in API call)

#### Weight Normalization
The system automatically normalizes weights to ensure they sum to approximately 1.0:

```python
# Example normalization
original_weights = {"sex": 0.3, "location": 0.4, "age": 0.2}
total = sum(original_weights.values())  # 0.9
normalized = {k: v/total for k, v in original_weights.items()}
# Result: {"sex": 0.33, "location": 0.44, "age": 0.22}
```

### Configuration Files Structure

```
src/config/
├── __init__.py              # Configuration loader
├── field_weights.yaml       # Weight configuration
└── services.yaml           # Service configuration
```

### API Configuration Endpoints

The system provides REST API endpoints for weight configuration management:

- `GET /api/weights/templates` - Get available weight templates
- `GET /api/weights/cultures` - Get culture-specific overrides
- `POST /api/weights/validate` - Validate custom weight configuration
- `POST /api/weights/calculate` - Calculate final weights with overrides

### MCP Configuration Tools

The system also provides MCP tools for weight configuration:

- `get_weight_templates` - Get available templates
- `get_culture_overrides` - Get culture-specific overrides
- `validate_weights` - Validate weight configuration
- `generate_identity` - Generate names with configurable weights

## 🧪 Testing

### True Positive Watchlist Validation Test

The system includes comprehensive testing for watchlist validation with known problematic names to ensure proper filtering and traceability.

```mermaid
graph TB
    subgraph "True Positive Test Method"
        START([Start True Positive Test]) --> INIT[Initialize WatchlistValidator]
        INIT --> TEST_NAMES[Define Test Names]
        
        subgraph "Test Names Selection"
            TEST_NAMES --> NAME1[Osama bin Laden<br/>Expected: OFAC SDN, FBI Most Wanted]
            TEST_NAMES --> NAME2[Saddam Hussein<br/>Expected: OFAC SDN, UN Sanctions]
            TEST_NAMES --> NAME3[Kim Jong-un<br/>Expected: UN Sanctions, OFAC SDN]
            TEST_NAMES --> NAME4[Vladimir Putin<br/>Expected: EU Sanctions, UK Sanctions]
            TEST_NAMES --> NAME5[Ted Bundy<br/>Expected: Radford DB, MAP]
        end
        
        NAME1 --> VALIDATE1[Validate Name 1]
        NAME2 --> VALIDATE2[Validate Name 2]
        NAME3 --> VALIDATE3[Validate Name 3]
        NAME4 --> VALIDATE4[Validate Name 4]
        NAME5 --> VALIDATE5[Validate Name 5]
        
        subgraph "Validation Process"
            VALIDATE1 --> CACHE1{Check Cache}
            VALIDATE2 --> CACHE2{Check Cache}
            VALIDATE3 --> CACHE3{Check Cache}
            VALIDATE4 --> CACHE4{Check Cache}
            VALIDATE5 --> CACHE5{Check Cache}
            
            CACHE1 -->|Cache Hit| RESULT1[Return Cached Result]
            CACHE2 -->|Cache Hit| RESULT2[Return Cached Result]
            CACHE3 -->|Cache Hit| RESULT3[Return Cached Result]
            CACHE4 -->|Cache Hit| RESULT4[Return Cached Result]
            CACHE5 -->|Cache Hit| RESULT5[Return Cached Result]
            
            CACHE1 -->|Cache Miss| SOURCES1[Check 17 Sources]
            CACHE2 -->|Cache Miss| SOURCES2[Check 17 Sources]
            CACHE3 -->|Cache Miss| SOURCES3[Check 17 Sources]
            CACHE4 -->|Cache Miss| SOURCES4[Check 17 Sources]
            CACHE5 -->|Cache Miss| SOURCES5[Check 17 Sources]
            
            subgraph "Validation Sources"
                SOURCES1 --> API1[API Calls]
                SOURCES2 --> API2[API Calls]
                SOURCES3 --> API3[API Calls]
                SOURCES4 --> API4[API Calls]
                SOURCES5 --> API5[API Calls]
                
                                 API1 --> SOURCE_LIST1["OFAC SDN, FBI, Interpol,<br/>UN Sanctions, EU Sanctions,<br/>UK Sanctions, Canada Sanctions,<br/>TSA No Fly, FINRA, Sex Offender,<br/>Dru Sjodin NSOPW, MAP,<br/>Radford DB, World-Check,<br/>Dow Jones, Public Records,<br/>Social Media"]
                 API2 --> SOURCE_LIST2["Same 17 Sources"]
                 API3 --> SOURCE_LIST3["Same 17 Sources"]
                 API4 --> SOURCE_LIST4["Same 17 Sources"]
                 API5 --> SOURCE_LIST5["Same 17 Sources"]
            end
            
            SOURCE_LIST1 --> AGGREGATE1[Aggregate Results]
            SOURCE_LIST2 --> AGGREGATE2[Aggregate Results]
            SOURCE_LIST3 --> AGGREGATE3[Aggregate Results]
            SOURCE_LIST4 --> AGGREGATE4[Aggregate Results]
            SOURCE_LIST5 --> AGGREGATE5[Aggregate Results]
            
            AGGREGATE1 --> STORE1[Store in Cache]
            AGGREGATE2 --> STORE2[Store in Cache]
            AGGREGATE3 --> STORE3[Store in Cache]
            AGGREGATE4 --> STORE4[Store in Cache]
            AGGREGATE5 --> STORE5[Store in Cache]
            
            STORE1 --> RESULT1
            STORE2 --> RESULT2
            STORE3 --> RESULT3
            STORE4 --> RESULT4
            STORE5 --> RESULT5
        end
        
        RESULT1 --> ANALYZE1[Analyze Results]
        RESULT2 --> ANALYZE2[Analyze Results]
        RESULT3 --> ANALYZE3[Analyze Results]
        RESULT4 --> ANALYZE4[Analyze Results]
        RESULT5 --> ANALYZE5[Analyze Results]
        
        subgraph "Result Analysis"
            ANALYZE1 --> CHECK1{Is Blocked?}
            ANALYZE2 --> CHECK2{Is Blocked?}
            ANALYZE3 --> CHECK3{Is Blocked?}
            ANALYZE4 --> CHECK4{Is Blocked?}
            ANALYZE5 --> CHECK5{Is Blocked?}
            
                         CHECK1 -->|Yes| BLOCKED1["✅ BLOCKED<br/>Sources: OFAC SDN, FBI<br/>Confidence: 0.95"]
             CHECK2 -->|Yes| BLOCKED2["✅ BLOCKED<br/>Sources: OFAC SDN, UN<br/>Confidence: 0.90"]
             CHECK3 -->|Yes| BLOCKED3["✅ BLOCKED<br/>Sources: UN, OFAC, EU<br/>Confidence: 0.92"]
             CHECK4 -->|Yes| BLOCKED4["✅ BLOCKED<br/>Sources: EU, UK, Canada<br/>Confidence: 0.88"]
             CHECK5 -->|Yes| BLOCKED5["✅ BLOCKED<br/>Sources: Radford, MAP<br/>Confidence: 0.95"]
             
             CHECK1 -->|No| CLEAR1["⚠️ NOT BLOCKED<br/>Sources Checked: 17<br/>Confidence: 0.00"]
             CHECK2 -->|No| CLEAR2["⚠️ NOT BLOCKED<br/>Sources Checked: 17<br/>Confidence: 0.00"]
             CHECK3 -->|No| CLEAR3["⚠️ NOT BLOCKED<br/>Sources Checked: 17<br/>Confidence: 0.00"]
             CHECK4 -->|No| CLEAR4["⚠️ NOT BLOCKED<br/>Sources Checked: 17<br/>Confidence: 0.00"]
             CHECK5 -->|No| CLEAR5["⚠️ NOT BLOCKED<br/>Sources Checked: 17<br/>Confidence: 0.00"]
        end
        
        BLOCKED1 --> COLLECT[Collect All Results]
        BLOCKED2 --> COLLECT
        BLOCKED3 --> COLLECT
        BLOCKED4 --> COLLECT
        BLOCKED5 --> COLLECT
        CLEAR1 --> COLLECT
        CLEAR2 --> COLLECT
        CLEAR3 --> COLLECT
        CLEAR4 --> COLLECT
        CLEAR5 --> COLLECT
    end
    
    subgraph "Traceability Report Generation"
        COLLECT --> STATS[Calculate Statistics]
        STATS --> DETAILED[Generate Detailed Results]
        DETAILED --> SOURCE_ANALYSIS[Source Effectiveness Analysis]
        SOURCE_ANALYSIS --> SAVE_JSON[Save JSON Report]
        SAVE_JSON --> CONCLUSION[Generate Conclusion]
    end
    
    subgraph "Expected vs Actual Results"
        CONCLUSION --> COMPARE{Compare Results}
                 COMPARE -->|Mock Test| SUCCESS["✅ SUCCESS<br/>5/5 Blocked (100%)<br/>High Confidence Matches"]
         COMPARE -->|Real Test| ISSUES["⚠️ ISSUES<br/>0/5 Blocked (0%)<br/>API Access Problems"]
    end
    
    SUCCESS --> RECOMMEND[Implementation Recommendations]
    ISSUES --> RECOMMEND
    
    RECOMMEND --> END([End Test])
    
    style START fill:#e1f5fe
    style END fill:#e8f5e8
    style SUCCESS fill:#c8e6c9
    style ISSUES fill:#ffcdd2
    style BLOCKED1 fill:#c8e6c9
    style BLOCKED2 fill:#c8e6c9
    style BLOCKED3 fill:#c8e6c9
    style BLOCKED4 fill:#c8e6c9
    style BLOCKED5 fill:#c8e6c9
    style CLEAR1 fill:#ffcdd2
    style CLEAR2 fill:#ffcdd2
    style CLEAR3 fill:#ffcdd2
    style CLEAR4 fill:#ffcdd2
    style CLEAR5 fill:#ffcdd2
```

#### Run True Positive Tests
```bash
# Run real API test (requires API keys)
python test_true_positive_watchlist.py

# Run mock test (demonstrates expected behavior)
python test_mock_true_positive.py
```

#### Test Results
- **Mock Test**: 100% success rate (5/5 names blocked)
- **Real Test**: 0% success rate (API access limitations)
- **Traceability**: Complete audit trail with JSON reports
- **Source Analysis**: Effectiveness metrics for all 17 sources

### Run All Tests
```bash
python -m pytest tests/
```

### Test Specific Components
```bash
# Test API endpoints
python tests/test_api_endpoints.py

# Test MCP connectivity
python test_mcp_connectivity.py

# Test Strands agents
python tests/test_strands_agent.py
```

### Manual Testing
```bash
# Test name generation
python -c "
import requests
data = {
    'category': 'person',
    'parameters': {
        'sex': 'Male',
        'location': 'USA',
        'age': '30',
        'occupation': 'Doctor',
        'race': 'Chinese',
        'fast_mode': True
    }
}
response = requests.post('http://localhost:8001/api/names/generate', json=data)
print('Generated Names:')
print(response.json()['result'])
"
```

## 📁 Project Structure

```
NAME/
├── src/                          # Core source code
│   ├── api/                      # FastAPI application
│   ├── core/                     # Core business logic
│   ├── config/                   # Configuration files
│   │   ├── field_weights.yaml    # Weight configuration
│   │   └── __init__.py           # Configuration loader
│   ├── database/                 # Database models and operations
│   ├── services/                 # AI services and MCP integration
│   │   ├── combined_service.py   # Combined MCP + API service
│   │   ├── mcp_service.py        # MCP service (legacy)
│   │   └── api_service.py        # API service (legacy)
│   └── utils/                    # Utilities and configuration
├── frontend/                     # React frontend application
│   ├── src/
│   │   ├── components/           # React components
│   │   └── ...
│   └── package.json
├── tests/                        # Test suite
├── docs/                         # Documentation
├── results/                      # Logs and results
├── start_combined_service.py     # Main startup script (recommended)
├── start_mcp_service.py          # MCP service startup (legacy)
├── start_api_service.py          # API service startup (legacy)
└── test_mcp_client.py            # Connectivity testing
```

## 🔍 API Reference

### Endpoints

#### `POST /api/generate-identity`
Generate culturally appropriate identities with configurable weights.

**Request Body:**
```json
{
  "sex": "string (required)",
  "location": "string (required)", 
  "age": "integer (required)",
  "occupation": "string (required)",
  "race": "string (required)",
  "religion": "string (required)",
  "birth_year": "integer (required)",
  "birth_country": "string (optional)",
  "citizenship_country": "string (optional)",
  "diaspora_generation": "integer (optional)",
  "custom_weights": {
    "sex": "float (optional)",
    "location": "float (optional)",
    "age": "float (optional)",
    "occupation": "float (optional)",
    "race": "float (optional)",
    "religion": "float (optional)",
    "birth_year": "float (optional)"
  },
  "template_name": "string (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "identities": [
    {
      "first_name": "string",
      "middle_name": "string",
      "last_name": "string",
      "full_name": "string"
    }
  ],
  "weights_used": {
    "sex": 0.25,
    "location": 0.20,
    "age": 0.15,
    "occupation": 0.10,
    "race": 0.20,
    "religion": 0.05,
    "birth_year": 0.05
  }
}
```

#### `GET /health`
Check system health status.

#### `GET /api/categories`
Get available name generation categories.

#### `GET /api/traceability/{request_id}`
Get traceability report for a request.

### MCP Tools

#### `generate_identity`
Generate culturally appropriate identities with configurable weights.

**Parameters:**
- `sex`: Gender (Male/Female/Non-binary)
- `location`: Geographic location
- `age`: Age
- `occupation`: Professional field
- `race`: Ethnicity/culture
- `religion`: Religious background
- `birth_year`: Year of birth
- `custom_weights`: Custom field weights (optional)
- `template_name`: Weight template to apply (optional)

#### `get_weight_templates`
Get available weight templates for different use cases.

**Returns:** Available templates (cultural_focus, geographic_focus, professional_focus, balanced)

#### `get_culture_overrides`
Get culture-specific weight overrides.

**Returns:** Culture-specific weight adjustments for different ethnicities.

#### `validate_weights`
Validate weight configuration.

**Parameters:**
- `field_weights`: Weight configuration to validate
- `culture_context`: Cultural context (optional)

## 🐛 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check running processes
tasklist | findstr python.exe

# Kill conflicting processes
taskkill /F /IM python.exe

# Restart combined service
.venv/Scripts/python.exe start_combined_service.py
```

#### Frontend Connection Issues
```bash
# Check combined service is running
curl http://localhost:8500/health

# Update frontend proxy if needed
# Edit frontend/package.json and update "proxy" field to "http://localhost:8500"
```

#### MCP Server Issues
```bash
# Test MCP connectivity
.venv/Scripts/python.exe test_mcp_client.py

# Check combined service logs
# Look for errors in console output

# Test MCP tools directly
curl -X POST http://localhost:8500/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}'
```

#### Slow Name Generation
- Ensure `fast_mode: true` is set in API requests
- Check Ollama is running and accessible
- Verify network connectivity for external services

### Logs and Debugging

#### Enable Debug Logging
```python
# In src/utils/logging_config.py
LOG_LEVEL = "DEBUG"
```

#### View Application Logs
```bash
# Check results/logs/app.log
tail -f results/logs/app.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Strands Framework**: For the multi-agent AI system
- **MCP Protocol**: For standardized agent communication
- **Ollama**: For local LLM processing
- **FastAPI**: For high-performance API development
- **React & Material-UI**: For the modern frontend interface

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` folder
- Review the troubleshooting section above

---

**Made with ❤️ for culturally appropriate name generation**
