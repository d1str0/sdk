package trinsic;

import org.junit.jupiter.api.Assertions;
import trinsic.okapi.DidException;
import trinsic.services.AccountService;
import trinsic.services.ProviderService;
import trinsic.services.common.v1.ProviderOuterClass;

import java.io.IOException;
import java.util.concurrent.ExecutionException;

public class EcosystemsDemo {
    public static void main(String[] args) throws IOException, DidException, ExecutionException, InterruptedException {
        run();
    }

    public static void run() throws IOException, DidException, ExecutionException, InterruptedException {
        var accountService = new AccountService(TrinsicUtilities.getTrinsicServiceOptions());
        var account = accountService.signIn().get();
        var service = new ProviderService(TrinsicUtilities.getTrinsicServiceOptions(account));

        var response = service.createEcosystem(ProviderOuterClass.CreateEcosystemRequest.newBuilder().setDescription("My ecosystem").setUri("https://example.com").build()).get();

        Assertions.assertNotNull(response.getEcosystem());
        Assertions.assertNotNull(response.getEcosystem().getId());
        Assertions.assertTrue(response.getEcosystem().getId().startsWith("urn:trinsic:ecosystems:"));

//        var actualList = service.listEcosystems(ProviderOuterClass.ListEcosystemsRequest.newBuilder().build()).get();
//        Assertions.assertNotNull(actualList);
//        Assertions.assertTrue(actualList.size() > 0);

        accountService.shutdown();
        service.shutdown();
    }
}
