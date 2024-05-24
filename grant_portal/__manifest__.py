{
  "name": "Grant Website",
  "description": "Allow website access to grant calls and application through portal.",
  "author": "Tamás Dombos",
  "license": "AGPL-3",
  "depends": [
    "grant",
    "portal",
    "website",
  ],
  "data": [
    "security/ir.model.access.csv",
    "security/grant_security.xml",
    "views/main_templates.xml",
    "views/portal_templates.xml",
    "views/views.xml",
    "data/config_data.xml",
  ],
  'assets': {
    'web.assets_frontend': [
        
    ]
    }
}
