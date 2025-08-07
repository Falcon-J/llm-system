@echo off
echo 🧪 Testing HackRx API with cURL
echo ================================

echo.
echo 🚀 Testing server health...
curl -s -o nul -w "Server status: %%{http_code}\n" http://localhost:8000/docs

echo.
echo 🎯 Testing HackRx endpoint...
echo This may take 30-60 seconds for document processing...
echo.

curl -X POST "http://localhost:8000/hackrx/run" ^
  -H "Authorization: Bearer hackrx-api-token-2024" ^
  -H "Content-Type: application/json" ^
  -d "{\"documents\": \"https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%%3A11%%3A24Z&se=2027-07-05T09%%3A11%%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%%2FjUHNO7HzQ%%3D\", \"questions\": [\"What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?\", \"Does this policy cover maternity expenses?\"]}" ^
  -w "\n\nResponse time: %%{time_total}s\nStatus code: %%{http_code}\n"

echo.
echo ✅ Test completed!
pause
