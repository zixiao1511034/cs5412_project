az login
az group create -n cow-id-function -l eastus
az storage account create -n cowstoragecloud -g cow-id-function --sku Standard_LRS
az storage queue create --name imagequeue --account-name cowstoragecloud 

az signalr create -n cow-signalr -g cow-id-function --sku Standard_S1 --unit-count 1 --service-mode Serverless

func azure functionapp publish imageclassify -b remote

{
      "type": "signalR",
      "name": "$return",
      "hubName": "cow-signalr",
      "direction": "out"
    }


az storage container create -n videoblob --account-name <stor name>
az storage container create -n pics --account-name <stor name>
az storage container create -n logging --account-name <stor name>


brew install
brew link --overwrite azure-functions-core-tools@3


brew install azure-functions-core-tools@2
https://cowimageclassify.azurewebsites.net/api/negotiate


https://stackoverflow.com/questions/43871637/no-access-control-allow-origin-header-is-present-on-the-requested-resource-whe

<policies>
    <inbound>
        <base />
        <cors allow-credentials="true">
            <allowed-origins>
                <origin>http://127.0.0.1:5500</origin>
            </allowed-origins>
            <allowed-methods>
                <method>GET</method>
                <method>POST</method>
            </allowed-methods>
            <allowed-headers>
                <header>*</header>
            </allowed-headers>
            <expose-headers>
                <header>*</header>
            </expose-headers>
        </cors>
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>