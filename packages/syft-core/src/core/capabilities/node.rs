use crate::core::worker::{get_config, Configurable};
use crate::proto::syftlib::config_server::Config;
pub use crate::proto::syftlib::{
    CapabilityReply, ConnectReply, ConnectRequest, NodeRequest, RegisterCapabilityRequest,
};
use tonic::{Request, Response, Status};

pub use crate::proto::syftlib::config_client::ConfigClient;
pub use crate::proto::syftlib::config_server::ConfigServer;

#[derive(Debug, Default)]
pub struct ConfigService {
    node_id: i32,
}

impl ConfigService {}

#[tonic::async_trait]
impl Config for ConfigService {
    async fn capabilities(
        &self,
        request: Request<NodeRequest>,
    ) -> Result<Response<CapabilityReply>, Status> {
        println!("Got a request: {:?}", request);

        let config = get_config().clone();

        let capabilities = config
            .lock()
            .unwrap()
            .capability_map
            .iter()
            .map(|(k, _v)| k.to_owned())
            .collect();

        let reply = CapabilityReply {
            capability: capabilities,
        };

        Ok(Response::new(reply))
    }

    async fn register_capability(
        &self,
        request: Request<RegisterCapabilityRequest>,
    ) -> Result<Response<CapabilityReply>, Status> {
        println!("Got a request: {:?}", request);

        let config = get_config().clone();
        //let cap = config.lock().unwrap();
        //     .add_capability(request.into_inner().capability_name, callback);

        let capabilities = config
            .lock()
            .unwrap()
            .capability_map
            .iter()
            .map(|(k, _v)| k.to_owned())
            .collect();

        let reply = CapabilityReply {
            capability: capabilities,
        };

        Ok(Response::new(reply))
    }

    async fn connect_peer(
        &self,
        request: Request<ConnectRequest>,
    ) -> Result<Response<ConnectReply>, Status> {
        let client_node_id = request.into_inner().client_node_id;

        let config = get_config();
        config.lock().unwrap().add_peer(client_node_id);
        let node_id = config.lock().unwrap().get_node_id();

        let reply = ConnectReply {
            node_id: node_id.clone(),
        };

        Ok(Response::new(reply))
    }
}
