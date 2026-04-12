#!/usr/bin/env python3
"""Comprehensive test suite for SUBIT-NOUS v4.0.0.

Run with: pytest tests/test_all.py -v
Or: python tests/test_all.py
"""

import os
import sys
import json
import tempfile
import subprocess
import unittest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from subit_nous.core import (
    text_to_subit, subit_to_name, get_mode, archetype_color,
    text_to_soft, cosine_similarity, interpolate_soft, soft_to_hard
)
from subit_nous.subit_algebra import Subit
from subit_nous.client import SubitClient


class TestCoreAlgebra(unittest.TestCase):
    """Test core SUBIT algebra."""

    def test_subit_creation(self):
        micro = Subit(0b10101010)
        macro = Subit(0b11111111)
        meso = Subit(0b01010101)
        meta = Subit(0b00000000)

        self.assertEqual(micro.bits, 170)
        self.assertEqual(macro.bits, 255)
        self.assertEqual(meso.bits, 85)
        self.assertEqual(meta.bits, 0)

    def test_xor_operation(self):
        micro = Subit(0b10101010)
        macro = Subit(0b11111111)
        xor_result = micro.xor(macro)
        self.assertEqual(xor_result.bits, 0b01010101)
        self.assertEqual(xor_result.to_human(), "MESO mode")

    def test_hamming_distance(self):
        micro = Subit(0b10101010)
        macro = Subit(0b11111111)
        self.assertEqual(micro.distance(macro), 4)
        self.assertEqual(micro.distance(micro), 0)

    def test_projection(self):
        micro = Subit(0b10101010)
        self.assertEqual(micro.project("WHO"), 0b10)
        self.assertEqual(micro.project("WHERE"), 0b10)
        self.assertEqual(micro.project("WHEN"), 0b10)
        self.assertEqual(micro.project("MODE"), 0b10)

    def test_flip_axis(self):
        micro = Subit(0b10101010)
        flipped = micro.flip_axis("WHO")
        self.assertEqual(flipped.bits, 0b00101010)

    def test_invert(self):
        micro = Subit(0b10101010)
        inverted = micro.invert()
        self.assertEqual(inverted.bits, 0b01010101)


class TestTextToSubit(unittest.TestCase):
    """Test text to SUBIT conversion."""

    def test_micro_mode(self):
        text = "I think logically about the east in spring"
        subit = text_to_subit(text)
        self.assertEqual(subit, 170)
        self.assertEqual(get_mode(subit), "MICRO")

    def test_macro_mode(self):
        text = "We trust our community in the south during summer"
        subit = text_to_subit(text)
        self.assertEqual(subit, 255)
        self.assertEqual(get_mode(subit), "MACRO")

    def test_meso_mode(self):
        text = "You feel the beauty of autumn in the west"
        subit = text_to_subit(text)
        self.assertEqual(subit, 85)
        self.assertEqual(get_mode(subit), "MESO")

    def test_meta_mode(self):
        text = "They exert power in the north during winter"
        subit = text_to_subit(text)
        self.assertEqual(subit, 0)
        self.assertEqual(get_mode(subit), "META")

    def test_empty_text(self):
        subit = text_to_subit("")
        self.assertEqual(subit, 170)

    def test_noise_text(self):
        subit = text_to_subit("1234567890!@#$%^&*()")
        self.assertEqual(subit, 170)


class TestSubitToName(unittest.TestCase):
    """Test archetype naming."""

    def test_special_modes(self):
        self.assertEqual(subit_to_name(0b10101010), "MICRO mode")
        self.assertEqual(subit_to_name(0b11111111), "MACRO mode")
        self.assertEqual(subit_to_name(0b01010101), "MESO mode")
        self.assertEqual(subit_to_name(0b00000000), "META mode")

    def test_mixed_archetype(self):
        self.assertEqual(subit_to_name(170), "MICRO mode")
        self.assertEqual(subit_to_name(255), "MACRO mode")


class TestContinuousSUBIT(unittest.TestCase):
    """Test soft vectors and continuous space."""

    def test_text_to_soft(self):
        text = "I think logically"
        soft = text_to_soft(text)
        self.assertEqual(len(soft), 8)
        self.assertTrue(all(-1 <= v <= 1 for v in soft))

    def test_cosine_similarity(self):
        text1 = "I think logically about the east in spring"
        text2 = "We trust our community in the south during summer"
        soft1 = text_to_soft(text1)
        soft2 = text_to_soft(text2)
        sim = cosine_similarity(soft1, soft2)
        self.assertAlmostEqual(sim, -0.0215, places=2)

    def test_cosine_similarity_self(self):
        text = "I think logically"
        soft = text_to_soft(text)
        sim = cosine_similarity(soft, soft)
        self.assertAlmostEqual(sim, 1.0, places=2)

    def test_interpolation(self):
        text1 = "I think logically"
        text2 = "We trust our community"
        soft1 = text_to_soft(text1)
        soft2 = text_to_soft(text2)
        interp = interpolate_soft(soft1, soft2, 0.5)
        self.assertEqual(len(interp), 8)
        expected = (soft1 + soft2) / 2
        for a, b in zip(interp, expected):
            self.assertAlmostEqual(a, b, places=5)

    def test_soft_to_hard(self):
        soft = text_to_soft("I think logically about the east in spring")
        hard = soft_to_hard(soft)
        self.assertIsInstance(hard, int)
        self.assertTrue(0 <= hard <= 255)


class TestClientSDK(unittest.TestCase):
    """Test Python SDK."""

    def setUp(self):
        self.client = SubitClient()

    def test_analyze(self):
        result = self.client.analyze("I think logically about the east in spring")
        self.assertEqual(result.subit, 170)
        self.assertEqual(result.archetype, "MICRO mode")
        self.assertEqual(result.mode, "MICRO")
        self.assertEqual(result.who, "ME")

    def test_to_subit(self):
        s = self.client.to_subit("I think logically")
        self.assertIsInstance(s, Subit)

    def test_xor(self):
        s1 = self.client.to_subit("I think logically")
        s2 = self.client.to_subit("We trust our community")
        xor_result = self.client.xor(s1, s2)
        self.assertIsInstance(xor_result, Subit)

    def test_distance(self):
        s1 = self.client.to_subit("I think logically")
        s2 = self.client.to_subit("We trust our community")
        dist = self.client.distance(s1, s2)
        self.assertIsInstance(dist, int)


class TestArchetypeColor(unittest.TestCase):
    """Test color mapping."""

    def test_colors(self):
        self.assertEqual(archetype_color(0b10101010), '#3498db')
        self.assertEqual(archetype_color(0b11111111), '#2ecc71')
        self.assertEqual(archetype_color(0b01010101), '#f1c40f')
        self.assertEqual(archetype_color(0b00000000), '#9b59b6')


class TestCLI(unittest.TestCase):
    """Test CLI commands."""

    def test_version(self):
        result = subprocess.run(
            ["nous", "version"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("SUBIT-NOUS version", result.stdout)

    def test_analyze_folder(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            file_path.write_text("I think logically about the east in spring", encoding='utf-8')

            result = subprocess.run(
                ["nous", "analyze", tmpdir, "--output", "test_cli_out"],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Graph built:", result.stdout)

            import shutil
            shutil.rmtree("test_cli_out", ignore_errors=True)

    def test_classify(self):
        result = subprocess.run(
            ["nous", "classify", "I think logically about the east"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("SUBIT:", result.stdout)


class TestClassifier(unittest.TestCase):
    """Test neural classifier (if model available)."""

    def test_classifier_import(self):
        try:
            from subit_nous.classifier import SubitClassifier
            self.assertTrue(True)
        except ImportError:
            self.skipTest("transformers not installed")

    def test_classifier_exists(self):
        model_path = Path("./subit_model")
        if model_path.exists():
            self.assertTrue((model_path / "config.json").exists())
        else:
            self.skipTest("Model not trained yet")


def run_tests():
    """Run all tests with unittest."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCoreAlgebra)
    suite.addTests(loader.loadTestsFromTestCase(TestTextToSubit))
    suite.addTests(loader.loadTestsFromTestCase(TestSubitToName))
    suite.addTests(loader.loadTestsFromTestCase(TestContinuousSUBIT))
    suite.addTests(loader.loadTestsFromTestCase(TestClientSDK))
    suite.addTests(loader.loadTestsFromTestCase(TestArchetypeColor))
    suite.addTests(loader.loadTestsFromTestCase(TestCLI))
    suite.addTests(loader.loadTestsFromTestCase(TestClassifier))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 60)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())