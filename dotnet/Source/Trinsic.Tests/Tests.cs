﻿using System;
using System.IO;
using System.Threading.Tasks;
using System.Xml;
using Newtonsoft.Json.Linq;
using Xunit;
using Xunit.Abstractions;

namespace Trinsic.Tests
{
    public class Tests
    {
        private readonly ITestOutputHelper _testOutputHelper;
        private const string ServerAddressName = "TRINSIC_SERVER_ADDRESS";

        public Tests(ITestOutputHelper testOutputHelper)
        {
            _testOutputHelper = testOutputHelper;
        }

        [Fact]
        public async Task TestWalletService()
        {
            var walletService = new WalletService(Environment.GetEnvironmentVariable(ServerAddressName));

            // SETUP ACTORS
            // Create 3 different profiles for each participant in the scenario
            var allison = await walletService.CreateWallet();
            var clinic = await walletService.CreateWallet();
            var airline = await walletService.CreateWallet();

            // Store profile for later use
            // File.WriteAllBytes("allison.bin", allison.ToByteString().ToByteArray());

            // Create profile from existing data
            // var allison = WalletProfile.Parser.ParseFrom(File.ReadAllBytes("allison.bin"));

            // ISSUE CREDENTIAL
            // Sign a credential as the clinic and send it to Allison
            walletService.SetProfile(clinic);

            var credentialJson = await File.ReadAllTextAsync("./vaccination-certificate-unsigned.jsonld");
            var credential = await walletService.IssueCredential(document: JObject.Parse(credentialJson));

            _testOutputHelper.WriteLine("Credential:");
            _testOutputHelper.WriteLine(credential.ToString(Newtonsoft.Json.Formatting.Indented));

            // STORE CREDENTIAL
            // Alice stores the credential in her cloud wallet.
            walletService.SetProfile(allison);

            var itemId = await walletService.InsertItem(credential);

            // SHARE CREDENTIAL
            // Allison shares the credential with the venue.
            // The venue has communicated with Allison the details of the credential
            // that they require expressed as a JSON-LD frame.
            walletService.SetProfile(allison);

            var proofRequestJson = File.ReadAllText("./vaccination-certificate-frame.jsonld");
            var credentialProof = await walletService.CreateProof(itemId, JObject.Parse(proofRequestJson));

            _testOutputHelper.WriteLine("Proof:");
            _testOutputHelper.WriteLine(credentialProof.ToString(Newtonsoft.Json.Formatting.Indented));


            // VERIFY CREDENTIAL
            // The airline verifies the credential
            walletService.SetProfile(airline);

            var valid = await walletService.VerifyProof(credentialProof);

            _testOutputHelper.WriteLine($"Verification result: {valid}");
            Assert.True(valid);
        }
    }
}