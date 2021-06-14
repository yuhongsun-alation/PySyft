use crate::core::worker::{get_config, Configurable};
use tonic::{Request, Response, Status};

pub use crate::proto::syftlib::greeter_client::GreeterClient;
pub use crate::proto::syftlib::greeter_server::GreeterServer;
pub use crate::proto::syftlib::{HelloReply, HelloRequest};
pub use crate::proto::syftlib::greeter_server::Greeter;

#[derive(Debug, Default)]
pub struct MyGreeter {}

#[tonic::async_trait]
impl Greeter for MyGreeter {
    async fn say_hello(
        &self,
        request: Request<HelloRequest>,
    ) -> Result<Response<HelloReply>, Status> {
        println!("Got a request: {:?}", request);

        let node_id = get_config().lock().unwrap().get_node_id();

        let reply = crate::proto::syftlib::HelloReply {
            message: format!("Hello {}! From Node {}", request.into_inner().name, node_id).into(),
        };

        Ok(Response::new(reply))
    }
}
